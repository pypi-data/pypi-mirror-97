import platform
if platform.linux_distribution()[0]:  # Import shared libraries before doing anything, only on linux
    import libpython
    libpython.init_libpython()
from swimbundle_utils.rest import *
from swimbundle_utils.flattener import *