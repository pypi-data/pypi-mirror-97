import time
import argparse

from ezca import Ezca

from ._util import split_channel_ifo
from .errors import CdsutilsError, CliError


DEFAULT_SETPOINT = 0.0
DEFAULT_GAIN = 1.0
DEFAULT_UGF = 1.0
DEFAULT_TIMEOUT = 0

DEFAULT_TIME_STEP = 0.01

summary = "servo EPICS channel with simple integrator (pole at zero)"

description_lib = """
args:

  'ezca' is initialized ezca object.

  'control' is primary control channel.

kwargs:

  'readback' is an optional separate channel to use as error signal.
  If not specified, 'control' is used as error channel.

  'setpoint' is the value to which the channel will be servoed
  (default={}).

  'gain' is gain between readback and control (default={}).

  'ugf' is a unity gain frequency in hertz (default={}).

  'timeout' is a time after which to terminate servo.  If 0, no
  timeout will be set (default).
""".format(DEFAULT_SETPOINT, DEFAULT_GAIN, DEFAULT_UGF)

##################################################

class Servo(object):
    __doc__ = """{}

    Separate readback/error channels are supported, as well as
    servoing two control channels with either common or differential
    actuation.

    Example, servo FOO to 0 by actuating on OFFSET:

    >>> servo = Servo(ezca, 'OFFSET', readback='FOO', setpoint=0)
    >>> servo.step()

    """.format(summary)

    def __init__(
            self, ezca, control,
            readback=None,
            setpoint=DEFAULT_SETPOINT,
            gain=DEFAULT_GAIN,
            ugf=DEFAULT_UGF,
            timeout=DEFAULT_TIMEOUT,
            control2=None,
            gain2=1.0,
    ):
        assert type(setpoint) in [int, float]
        assert type(gain) in [int, float]
        assert type(ugf) in [int, float]
        assert type(timeout) in [int, float]
        assert type(gain2) in [int, float]

        self._ezca = ezca
        self._readback = readback
        self._setpoint = setpoint

        self._chan1 = control
        self._gain = gain
        self._ugf = ugf
        self._chan2 = control2
        self._gain2 = gain2

        self._ctrl1 = 0
        self._ctrl2 = 0

        self._timeout = timeout

        self._t0 = None
        self._last_time = None
        self._done = False

    __init__.__doc__ = """
{}
  'control2' is an optional second control channel, and 'gain2' is the
  relative gain between 'control' and 'control2' (use 1 for common or
  -1 for differential).
""".format(description_lib)

    def step(self):
        """step the servo

        Amount of step depends on time since last step().

        """
        if self._done:
            return True

        current_time = time.time()

        # if this is the first step, set up initial values
        if self._last_time is None:
            self._t0 = current_time
            self._last_time = current_time
            self._ctrl1 = self._ezca[self._chan1]
            if self._chan2:
                self._ctrl2 = self._ezca[self._chan2]

        ctrl1_current = self._ezca.read(self._chan1, use_monitor=False)
        if ctrl1_current != self._ctrl1:
            raise CdsutilsError("Channel {} changed during step: {} != {}".format(
                self._chan1,
                ctrl1_current,
                self._ctrl1))
        if self._chan2:
            ctrl2_current = self._ezca.read(self._chan2, use_monitor=False)
            if ctrl2_current != self._ctrl2:
                raise CdsutilsError("Channel {} changed during step: {} != {}".format(
                    self._chan2,
                    ctrl2_current,
                    self._ctrl2))

        if self._readback:
            err = self._ezca[self._readback]
        else:
            # use control signal as error point
            if self._chan2:
                err = (self._ctrl1 + self._gain2 * self._ctrl2) / (1 + abs(self._gain2))
            else:
                err = self._ctrl1

        err -= self._setpoint

        dt = current_time - self._last_time
        self._last_time = current_time

        # calculate and set new control signals
        ctrl = self._gain * self._ugf * dt * err
        self._ctrl1 -= ctrl
        self._ezca[self._chan1] = self._ctrl1
        if self._chan2:
            self._ctrl2 -= self._gain2 * ctrl
            self._ezca[self._chan2] = self._ctrl2

        if self._timeout > 0 and current_time >= self._t0 + self._timeout:
            self._done = True
            return True

        return False

##################################################

def servo(*args, **kwargs):
    servo = Servo(*args, **kwargs)
    while not servo.step():
        time.sleep(DEFAULT_TIME_STEP/10)

servo.__doc__ = """{}

*args and **kwargs are passed directly to Servo(), with the following
 arguments supported:
{}
Example, servo FOO to 0 by actuating on OFFSET:

>>> servo(ezca, 'OFFSET', readback='FOO', setpoint=0)

""".format(summary, description_lib)

##################################################

def main():
    parser = argparse.ArgumentParser(
        description=summary,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'control',
        help="control channel")
    parser.add_argument(
        '-r', '--readback',
        help="readback (error) channel (default is control)")
    parser.add_argument(
        '-g', '--gain', type=float,
        default=DEFAULT_GAIN,
        help="gain between readback and channel (default={})".format(DEFAULT_GAIN))
    parser.add_argument(
        '-u', '--ugf', type=float,
        default=DEFAULT_UGF,
        help="unity gain frequency in hertz (default={})".format(DEFAULT_UGF))
    parser.add_argument(
        '-s', '--setpoint', type=float,
        default=DEFAULT_SETPOINT,
        help="set point value (default={})".format(DEFAULT_SETPOINT))
    parser.add_argument(
        '-t', '--timeout', type=float,
        default=DEFAULT_TIMEOUT,
        help="timeout in seconds (default={})".format(DEFAULT_TIMEOUT))
    cgroup = parser.add_mutually_exclusive_group()
    cgroup.add_argument(
        '-c', '--comm',
        help="2nd control channel, common")
    cgroup.add_argument(
        '-d', '--diff',
        help="2nd control channel, differential")
    args = parser.parse_args()

    control2 = None
    gain2 = 1
    if args.comm:
        __, control2 = split_channel_ifo(args.comm)
    elif args.diff:
        __, control2 = split_channel_ifo(args.diff)
        gain2 = -1

    try:
        servo(Ezca(),
              args.control,
              args.readback,
              args.setpoint,
              args.gain,
              args.ugf,
              args.timeout,
              control2,
              gain2)
    except CdsutilsError as e:
        CliError(e)
