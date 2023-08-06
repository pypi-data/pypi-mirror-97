# --- Common Functionality

import re


def escape_path( path ):
    # normalize slashes
    path = re.sub( r'(?:/|\\\\|\\)', '/', path )

    # quote for spaces
    path = f'"{ path }"'
    return path
