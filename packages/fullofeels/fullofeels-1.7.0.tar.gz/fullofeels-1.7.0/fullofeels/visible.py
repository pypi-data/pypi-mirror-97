
#   Hugh Fisher, Canberra Australia
#   Released under the MIT license

"""fullOfEels utility code that is visible to module writers as
        import fullofeels
   These are only necessary for some argument conversion options
   and for specifying object descriptors (properties)"""

# NOTE: these are entirely standalone, so you can copy this particular
# module (as fullofeels.py, NOT visible.py) anywhere you like

import sys

def argumentConverter(proc):
    """Decorator that identifies proc as Python to C argument converter"""
    proc._foeelsArgumentConverter = True
    return proc

# Python 3.1 and later have built in converter from Python string to
# local file system compatible path
if sys.version_info >= (3, 1):
    def fileSystemPath(str, addr):
        pass
    fileSystemPath.cName = "PyUnicode_FSConverter"
    fileSystemPath._foeelsArgumentConverter = True
