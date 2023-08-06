from .__version__ import __version__

########################################
# USAGE: To add a new module function and/or command line interface,
# add the following:

# For modules that include command line interfaces, append the module
# to the CMDS list.

# otherwise, import the need functions or classes here, catching
# import errors in case their dependencies are not locally met
########################################

CMDS = [
    'read',
    'write',
    'switch',
    'sfm',
    'step',
    'servo',
    'trigservo',
    'avg',
    'audio',
    'water',
    ]

try:
    from .step import step, Step
except ImportError:
    pass

try:
    from .servo import servo, Servo
except ImportError:
    pass

try:
    from .trigservo import trigservo
except ImportError:
    pass

try:
    from .getdata import getdata
except ImportError:
    pass

try:
    from .avg import avg
except ImportError:
    pass

from .matrix import CDSMatrix
