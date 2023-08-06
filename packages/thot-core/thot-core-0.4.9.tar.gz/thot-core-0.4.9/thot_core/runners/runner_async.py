#!/usr/bin/env python
# coding: utf-8

# --- Async Runner [Core]

import os
import json
import signal
import platform
import asyncio
import logging
import threading
import subprocess
from time import perf_counter
from functools import partial

from . import common
from ..classes.container import Container


class Runner:
    """
    For performing analysis on a Thot project.

    Hooks are:
        + get_container: Method to retrieve the Container being run.
            Provided the root id, should return the Container.
            [Required]

        + get_script_info: Method to retrieve require information about the Script being run.
            [Signature: ( ScriptAssociation.script ) => ( script id, script path ) ]
            [Required]

        + script_error: Runs when a Script creates an error.
            [Signature: ( error, script_id, root, ignore_errors ) => ()]
            :param err: The raise error.
                err.cmd contains Container and Script info.
                err.output contains the traceback.
            :param script_id: Id of the Script. [Default: None]
            :param root: Container of error. [Default: None]
            :param ignore_errors: Whether to ignore errors. [Default: False]

        + assets_added: Run after a Script analysis is complete, passed ids of the added Assets.
            [Signature: ( added_assets ) => ()]

        + complete: Run after a subtree completes.
            [Signature: () => ()]
    """

    def __init__( self ):
        """
        Initializes a new Runner.
        """
        self.hooks = {
            'get_container':   None,
            'get_script_info': None,
            'script_error':    self._default_script_error_handler,
            'assets_added':    None,
            'complete':        None
        }

        self._procs = {}
        self._semaphore = None
        self._exit_task = None

        self._set_asyncio_event_loop_policy()


    def register( self, hook, method ):
        """
        Registers a hook method.

        :param hook: Name of the hook to register.
        :param method: Method to run.
        """
        if hook not in self.hooks:
            # hook is invalid,
            # all hook names are defined in constructor
            raise ValueError( 'Invalid hook name.' )

        self.hooks[ hook ] = method


    @property
    def semaphore( self ):
        """
        :returns: Semaphore.
        """
        return self._semaphore


    def set_semaphore( self, value ):
        """
        Sets the semaphore to use.

        :param value: Semaphore's value.
        :raises RuntimeError: If semaphore is already set.
        :raises TypeError: If semaphore is invalid.
        """
        if self._semaphore is not None:
            raise RuntimeError( 'Semaphore already set.' )

        self._semaphore = asyncio.Semaphore( value )

    # TODO [2]: Allow running between certain depths.
    async def eval_tree(
        self,
        root,
        tasks = None,
        **eval_args
    ):
        """
        Runs scripts on the Container tree.
        Uses DFS, running from bottom up.

        :param root: Container or id.
        :param tasks: Maximum number of tasks.
            If None, no limit. [Default: None]
        :param **eval_args: Arguments passed to #eval_container.
        :raises RuntimeError: If more than one of
            multithread, asynchronous, or multiprocess evaluates to True.
        """
        # signal handlers
        self._check_hooks()
        if threading.current_thread() is threading.main_thread():
            self._register_signal_handlers()

        # verbose
        verbose = self.get_kwarg( 'verbose', eval_args, False )
        if verbose:
            logger = logging.getLogger( __name__ )
            subtree_start = perf_counter()

        # tasks
        # task validity
        if (
            isinstance( tasks, bool ) or
            not (
                ( tasks is None ) or
                isinstance( tasks, int )
            )
        ):
            raise TypeError( 'Parameter tasks must be None or an integer.' )

        if (
            isinstance( tasks, int ) and
            tasks < 1
        ):
            raise ValueError( 'Must allow at least one task, provided in tasks parameter.' )

        semaphore_creator = False
        if ( tasks is not None ) and ( self.semaphore is None ):
            # create semaphore
            self.set_semaphore( tasks )
            semaphore_creator = True

        # get root
        root = self.hooks[ 'get_container' ]( root )
        if not isinstance( root, Container ):
            root = Container( **root )

        # evaluate children
        children = []
        for child in root.children:
            child_task = self.eval_tree(
                child,
                tasks = tasks,
                **eval_args
            )

            children.append( child_task )

        try:
            await asyncio.gather( *children )

        except asyncio.CancelledError as err:
            return

        # evaluate self
        await self.eval_container( root, **eval_args )

        if self.hooks[ 'complete' ]:
            self.hooks[ 'complete' ]()

        if semaphore_creator:
            # destroy semaphore
            self._semaphore = None

        if verbose:
            logger.info( f'[Container { root._id }] { perf_counter() - subtree_start } s' )


    def eval_tree_sync(
        self,
        root,
        tasks = None,
        **eval_args
    ):
        """
        Evaluate tree.
        Convenience method so caller does now have to
        invoke asyncio themselves.

        See #eval_tree for description.
        """
        asyncio.run( self.eval_tree( root, tasks = tasks, **eval_args ) )


    async def eval_container(
        self,
        container,
        scripts = None,
        ignore_errors = False,
        verbose       = False
    ):
        """
        Evaluates Scripts on a Container.

        :param container: Container to evaluate.
        :param scripts: List of scripts to run, or None for all. [Default: None]
        :param ignore_errors: Continue running if an error is encountered. [Default: False]
        :param verbose: Log evaluation information. [Default: False]
        """

        # TODO [1]: Check filtering works.
        # filter scripts to run
        run_scripts = (
            container.scripts
            if scripts is None else
            self.filter_scripts( container.scripts, scripts )
        )

        # group scripts by priority
        priority_groups = self.group_scripts( run_scripts )
        priorities = list( priority_groups.keys() )
        priorities.sort()
        for p in priorities:
            assocs = priority_groups[ p ]

            try:
                await self.run_scripts(
                    container,
                    assocs,
                    ignore_errors = ignore_errors,
                    verbose = verbose
                )

            except asyncio.CancelledError as err:
                break


    async def run_scripts(
        self,
        container,
        associations,
        ignore_errors = False,
        verbose = False
    ):
        """
        Run given Scripts over the Cotnainer.

        :param container: Container.
        :param associations: ScriptAssociations to run.
        :param ignore_errors: Ignore errors during run. [Default: False]
        :param verbose: Verbose logging. [Default: False]
        """
        logger = logging.getLogger( __name__ )

        async def _run_script( association ):
            """
            Runs the given Script.

            :param association: ScriptAssociation to run.
            """
            async def _execute_script( script_id, script_path ):
                """
                :param script_id:
                :param script_path:
                :returns:
                """
                if verbose:
                    logger.info( f'Running script {script_id} on container {container._id}' )
                    eval_start = perf_counter()

                try:
                    script_assets = await self.run_script(
                        str( script_id ),  # convert ids if necessary
                        script_path,
                        str( container._id )
                    )

                except subprocess.CalledProcessError as err:
                    # check for keyboard interupt
                    sigint_pattern = 'died with <Signals.SIGINT: 2>'
                    if sigint_pattern in str( err ):
                        raise asyncio.CancelledError

                    # other error
                    self.hooks[ 'script_error' ]( err, script_id, container, ignore_errors )

                    # TODO [1]: Asset creation not tracked
                    #           if error occurs after an asset is created.
                    #           For now if an error occurs, do not track Asset
                    #           creation.
                    script_assets = ''


                except asyncio.CancelledError as err:
                    raise err

                if verbose:
                    logger.info(
                        f'[Container { container._id } | Script { script_id }] { perf_counter() - eval_start } s'
                    )

                return script_assets


            ( script_id, script_path ) = self.hooks[ 'get_script_info' ]( association.script )

            # execute script
            if self.semaphore is None:
                script_assets = await _execute_script( script_id, script_path )

            else:
                async with self.semaphore:
                    script_assets = await execute_script( script_id, script_path )

            if self.hooks[ 'assets_added' ]:
                script_assets = [
                    json.loads( asset ) for asset
                    in script_assets.decode().split( '\n' )
                    if asset
                ]

                self.hooks[ 'assets_added' ]( script_assets )


        # eval container
        tasks = []
        for association in associations:
            if not association.autorun:
                continue

            task = asyncio.create_task( _run_script( association ) )
            tasks.append( task )

        try:
            results = await asyncio.gather( *tasks )

        except asyncio.CancelledError as err:
            raise err


    async def run_script( self, script_id, script_path, container_id ):
        """
        Runs the given program on the given Container asynchronously.

        :param script_id: Id of the script.
        :param script_path: Path to the script.
        :param container: Id of the container to run from.
        :returns: Script output. Used for collecting added assets.
        """
        # TODO [0]: Ensure safely run
        # run program
        env = self.create_thot_env( container_id, script_id )
        script_path = common.escape_path( script_path )
        cmd = f'python { script_path }'
        proc = await asyncio.create_subprocess_shell(
            cmd,
            env = env,
            stdout = asyncio.subprocess.PIPE,
            stderr = asyncio.subprocess.PIPE
        )

        self._procs[ proc.pid ] = proc
        stdout, stderr = await proc.communicate()

        try:
            await proc.wait()

        finally:
            del self._procs[ proc.pid ]

        if stderr:
            err = subprocess.CalledProcessError(
                proc.returncode,
                f'[{ container_id }] { cmd }',
                stderr = stderr
            )

            raise err

        return stdout


    # --- helpers ---

    def _check_hooks( self ):
        """
        Verifies registered hooks.

        :returns: True
        :raises RuntimeError: If registered hooks are invalid.
        """
        if not self.hooks[ 'get_container' ]:
            raise RuntimeError( 'Required hook get_container is not set.' )

        if not self.hooks[ 'get_script_info' ]:
            raise RuntimeError( 'Required hook get_script_info is not set.' )

        return True


    def filter_scripts( self, associations, scripts ):
        """
        Filters scripts.

        :param associations: List of ScriptAssociations to filter.
        :param scripts: List of Scripts to run.
        :returns: List of filtered ScriptAssociations.
        """
        def _filter_script( association, scripts ):
            """
            :param association: ScriptAssociation to filter.
            :param scripts: List of valid Script ids.
            :returns: True if association's script's id is in scripts, False oherwise.
            """
            ( script_id, _) = self.hooks[ 'get_script_info' ]( association.script )
            return ( script_id in scripts )


        filtered = filter(
            lambda assoc: _filter_script( assoc, scripts ),
            associations
        )

        return filtered


    async def _terminate_procs( self, sig = signal.SIGINT ):
        procs = []
        for _, proc in self._procs.items():
            try:
                proc.send_signal( sig )

            except ProcessLookupError as err:
                # process already dead
                continue

            else:
                procs.append( proc.wait() )

        await asyncio.gather( *procs )


    async def _exit_tasks( self, sig ):
        """
        End all tasks.

        :param sig: Signal to end processes with.
        """
        print( '\nWrapping up, please wait...' )

        # end all processes
        await self._terminate_procs( sig )

        # cancel tasks
        loop = asyncio.get_running_loop()
        for task in asyncio.all_tasks( loop ):
            task.cancel()

        await self._exit_task


    def _set_asyncio_event_loop_policy( self ):
        """
        Sets asyncio event loop policy.
        
        In some versions of Python (3.7.0 - 3.7.8) asyncio#create_subprocess_shell
        raises a NotImplementedError on windows machines using
        the default policy. 

        This changes to a Proactor loop policy to prevent this error.

        See https://stackoverflow.com/questions/53127248/asyncio-create-subprocess-shell-python-3-7-on-windows
        for more info.
        """
        if platform.system() == 'Windows':
            # change asyncio event loop policy to proactor if needed
            try:
                asyncio.run( asyncio.create_subprocess_shell( '' ) )

            except NotImplementedError as err:
                # change to proactor loop
                asyncio.set_event_loop_policy( asyncio.WindowsProactorEventLoopPolicy() )


    def _register_signal_handlers( self ):
        """
        """
        def _exit( sig, loop ):
            # prevent further logging
            logger = logging.getLogger( __name__ )
            logger.disabled = True

            self._exit_task = loop.create_task( self._exit_tasks( sig ) )

        if platform.system() == 'Windows':
            # signal handlers do not exist on windows
            # TODO [1]: Add signal handling for Windows.
            return

        loop = asyncio.get_running_loop()
        for signame in { 'SIGINT', 'SIGTERM' }:
            sig = getattr( signal, signame )

            loop.add_signal_handler(
                sig,
                partial( _exit, sig, loop )
            )


    @staticmethod
    def group_scripts( associations ):
        """
        Groups ScriptAssociations by priority.

        :param scripts: List of ScriptAssociations.
        :returns: Dictionary keyed by priority with values a list of Script Associations.
        """
        groups = {}
        for assoc in associations:
            p = assoc.priority
            if p not in groups:
                # initialize priority group
                groups[ p ] = []

            groups[ p ].append( assoc )

        return groups


    @staticmethod
    def _default_script_error_handler(
        err,
        script_id = None,
        root = None,
        ignore_errors = False
    ):
        """
        :param err: The raise error.
            err.cmd contains Container and Script info.
            err.stderr contains the traceback.
        :param script_id: Id of the Script. [Default: None]
        :param root: Container of error. [Default: None]
        :param ignore_errors: Whether to ignore errors. [Default: False]
        """
        msg = f'{ err.cmd }\n{ err.stderr.decode() }\n'
        if ignore_errors:
            # TODO [2]: Only return errors after final exit.
            # collect errors for output at end
            print( msg )

        else:
            err.cmd = msg
            raise err


    @staticmethod
    def create_thot_env( container_id, script_id ):
        """
        Create the environment to run Thot.

        :param container_id:
        :param script_id:
        :returns: Thot environment.
        """
        env = os.environ.copy()
        env[ 'THOT_CONTAINER_ID' ] = container_id  # set root container to be used by thot library
        env[ 'THOT_SCRIPT_ID' ]    = script_id     # used in project for adding Assets

        return env

        
    @staticmethod
    def get_kwarg( key, kwargs, default = None):
        """
        Returns the values of a key in a dictionary if it exists,
        otherwise returns the default value.

        :param key: Key to retrieve.
        :param kwargs: Dictionary.
        :param default: Default value. [Default: None]
        :returns: Value of key or default value.
        """
        return kwargs[ key ] if ( key in kwargs ) else default
