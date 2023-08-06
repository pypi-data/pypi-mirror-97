#!/usr/bin/env python
# coding: utf-8

# --- Multithread Runner [Core]

import os
import sys
import json
import queue
import signal
import asyncio
import threading
import logging
import subprocess
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait

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



    def run_script( self, script_id, script_path, container_id ):
        """
        Runs the given program form the given Container.

        :param script_id: Id of the script.
        :param script_path: Path to the script.
        :param container: Id of the container to run from.
        :returns: Script output. Used for collecting added assets.
        """
        # setup environment
        env = os.environ.copy()
        env[ 'THOT_CONTAINER_ID' ] = container_id # set root container to be used by thot library
        env[ 'THOT_SCRIPT_ID' ]    = script_id    # used in project for adding Assets

        # TODO [0]: Ensure safely run
        # run program
        script_path = common.escape_path( script_path )
        try:
            return subprocess.check_output(
                f'python { script_path }',
                shell = True,
                env = env,
                stderr = subprocess.STDOUT
            )

        except subprocess.CalledProcessError as err:
            err.cmd = f'[{ container_id }] { err.cmd }'
            raise err


    # TODO [2]: Allow running between certain depths.
    def eval_tree(
        self,
        root,
        scripts = None,
        ignore_errors = False,
        multithread   = False,
        asynchronous  = False,
        multiprocess  = False,
        verbose       = False
    ):
        """
        Runs scripts on the Container tree.
        Uses DFS, running from bottom up.

        :param root: Container.
        :param scripts: List of scripts to run, or None for all. [Default: None]
        :param ignore_errors: Continue running if an error is encountered. [Default: False]
        :param multithread: Evaluate tree using multiple threads.
            True to use default number of threads, or an integer
            to specify how many threads to use.
            If interpreted as boolean is False, will use a single thread.
            Should be used for IO bound evaluations.
            CAUTION: May decrease runtime, but also locks system and can not kill.
            [Default: False] [Default Threads: 5]
        :param asynchronous: Evaluate tree asynchronously. [Default: False]
        :param multiprocess: Evaluate tree using multiple processes.
            Should be used for CPU bound evaluations.
            NOT YET IMPLEMENTED
            [Default: False]
        :param verbose: Log evaluation information. [Default: False]
        :raises RuntimeError: If more than one of
            multithread, asynchronous, or multiprocess evaluates to True.
        """
        self._check_hooks()

        root = self.hooks[ 'get_container' ]( root )
        if not isinstance( root, Container ):
            root = Container( **root )

        # eval children
        if verbose:
            subtree_start = perf_counter()

        kwargs = {
            'scripts': scripts,
            'ignore_errors': ignore_errors,
            'multithread': multithread,
            'verbose': verbose
        }

        # check eval specifications
        if sum( map( bool, [ multithread, asynchronous, multiprocess ] ) ) > 1:
            raise RuntimeError( 'Invalid evaluation specification. Only one of multithread, asynchronous, or multiprocess can evaluate to True.' )

        if asynchronous:
            raise NotImplementedError( 'Asynchronous evaluation is not yet implemented.' )

        elif multithread is not False:
            executor_creator = False
            if not isinstance( multithread, ThreadPoolExecutor ):
                def _kill_threads( executor ):
                    print( '\nWrapping up, please wait...' )

                    py_version = sys.version_info
                    if (
                        ( py_version.major < 3 ) or
                        ( ( py_version.major == 3 ) and ( py_version.minor < 9 ) )
                    ):
                        # py versions less than 3.9
                        # Executor#shutdown does not accept
                        # cancel_futures keyword
                        # manually shutdown

                        executor.shutdown( wait = False )
                        while True:
                            try:
                                work_item = executor._work_queue.get_nowait()

                            except queue.Empty:
                                break

                            if work_item is not None:
                                work_item.future.cancel()

                    else:
                        executor.shutdown( cancel_futures = True )

                    sys.exit( 0 )

                # create thread pool if needed
                max_workers = (
                    5 # default
                    if multithread is True else
                    multithread
                )

                multithread = ThreadPoolExecutor( max_workers = max_workers )
                kwargs[ 'multithread' ] = multithread
                executor_creator = True

                if threading.current_thread() is threading.main_thread():
                    signal.signal(
                        signal.SIGINT,
                        lambda sig, frame: _kill_threads( multithread )
                    )

            # can not use executor#map because child ownership seems to get messed up
            futures = list( map(
                lambda child: multithread.submit( self.eval_tree, child, **kwargs ),
                root.children
            ) )

            ( done, not_done ) = wait( futures )


            if executor_creator:
                multithread.shutdown()

        elif multiprocess is not False:
            raise NotImplementedError( 'Multiprocess evaluation is not yet implemented.' )

            executor_creator = False
            if not isinstance( multiprocess, ProcessPoolExecutor ):
                # create thread pool if needed
                max_workers = (
                    5 # default
                    if multiprocess is True else
                    multiprocess
                )

                multiprocess = ProcessPoolExecutor( max_workers = max_workers )
                kwargs[ 'multiprocess' ] = multiprocess
                executor_creator = True

            multiprocess.map(
                lambda child: self.eval_tree( child, **kwargs ),
                root.children
            )

            if executor_creator:
                multiprocess.shutdown()

        else:
            for child in root.children:
                # recurse
                self.eval_tree( child, **kwargs )

        # TODO [1]: Check filtering works.
        # filter scripts to run
        root.scripts.sort()
        run_scripts = (
            root.scripts
            if scripts is None else
            filter( lambda assoc: assoc.script in scripts, root.scripts ) # filter scripts
        )

        # eval self
        # TODO [0]: Group scripts by priority.
        #     Run scripts within each group asynchronously, or with multiprocessing.
        added_assets = []
        for association in run_scripts:
            if not association.autorun:
                continue

            ( script_id, script_path ) = self.hooks[ 'get_script_info' ]( association.script )

            if verbose:
                logging.info( 'Running script {} on container {}'.format( script_id, root._id )  )

            try:
                if verbose:
                    eval_start = perf_counter()

                script_assets = self.run_script(
                    str( script_id ), # convert ids if necessary
                    script_path,
                    str( root._id )
                )

                if verbose:
                    logging.info( f'[Container { root._id } | Script { script_id } ] { perf_counter() - eval_start } s' )


            except Exception as err:
                self.hooks[ 'script_error' ]( err, script_id, root, ignore_errors )

            if self.hooks[ 'assets_added' ]:
                script_assets = [
                    json.loads( asset ) for asset
                    in script_assets.decode().split( '\n' )
                    if asset
                ]

                self.hooks[ 'assets_added' ]( script_assets )

        if self.hooks[ 'complete' ]:
            self.hooks[ 'complete' ]()

        if verbose:
            logging.info( f'[Container { root._id }] { perf_counter() - subtree_start } s' )


    def _check_hooks( self ):
        """
        Verifies registered hooks.

        :throws: Error if registered hook is invalid.
        """
        if not self.hooks[ 'get_container' ]:
            raise RuntimeError( 'Required hook get_container is not set.' )

        if not self.hooks[ 'get_script_info' ]:
            raise RuntimeError( 'Required hook get_script_info is not set.' )


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
            err.output contains the traceback.
        :param script_id: Id of the Script. [Default: None]
        :param root: Container of error. [Default: None]
        :param ignore_errors: Whether to ignore errors. [Default: False]
        """
        msg = f'{ err.cmd }\n{ err.output.decode() }\n'
        if ignore_errors:
            # TODO [2]: Only return errors after final exit.
            # collect errors for output at end
            print( msg )

        else:
            err.cmd = msg
            raise err
