import sys
import time
import argparse

from ezca import Ezca

from ._util import split_channel_ifo
from .errors import CdsutilsError, CliError


DEFAULT_TIME_STEP = 0.1

summary = "step EPICS channels over specified range"

description_common = """'channel' is EPICS channel to step, and 'steps' is a step
specification in the following format:

  <step_spec>[,<number>]
  (<step_spec>,...)

where <step_spec> can be:

  +1.0 - linear up
  -1.0 - linear down
  *2.0 - geometric up
  /2.0 - geometric down
  +3dB - geometric dB up
  -3dB - geometric dB down

examples:

  '+1.0,4' - linear up, four steps of 1
  '(*3,*10,*30,*100)' - four steps of 3, 10 30, and 100
"""

##################################################

class SingleStep(object):
    def __init__(self, step):
        self._str = step.strip()
        self._operator = None
        self._size = None
        s = self._str
        if 'db' in s.lower():
            if s[0] == '-':
                dB = float(s[1:].lower().strip('db'))
                self._size = 10**(dB/20.0)
                self._operator = '/'
            elif s[0] == '+':
                dB = float(s[1:].lower().strip('db'))
                self._size = 10**(dB/20.0)
                self._operator = '*'
            else:
                dB = float(s.lower().strip('db'))
                self._size = 10**(dB/20.0)
                self._operator = '*'
        elif s[0] in ['+', '-']:
            self._operator = '+'
            self._size = float(s)
        elif s[0] == '*':
            self._operator = '*'
            self._size = float(s[1:])
        elif s[0] == '/':
            self._operator = '/'
            self._size = float(s[1:])
        else:
            self._operator = '+'
            self._size = float(s)

        if self._operator is None:
            raise CdsutilsError("Unable to parse step specification.")

    def __repr__(self):
        return self._str

    def __str__(self):
        return "{}('{}')".format(self.__class__.__name__, self._str)

    def __call__(self, value):
        return eval('{} {} {}'.format(value, self._operator, float(self._size)))


class Step(object):
    """step EPICS channel over specified range

Example:

>>> step = Step(ezca, 'GAIN1', '+1,10')
>>> step.step()

    """
    def __init__(self, ezca, channel, steps, time_step=DEFAULT_TIME_STEP):
        self._ezca = ezca
        self._channel = channel
        self._steps = steps
        try:
            self._time_step = float(time_step)
        except ValueError as e:
            raise CdsutilsError(e)
        if self._time_step <= 0:
            raise CdsutilsError("Step time_step must be positive definite.")

        # parse step string
        steps = steps.strip().strip('"').strip("'")
        if '(' in steps:
            try:
                temp_array = steps.lstrip('(').rstrip(')').split(',')
                self._step_array = [SingleStep(step) for step in temp_array]
            except ValueError as e:
                raise CdsutilsError("Invalid steps description.")
        elif ',' in steps:
            try:
                step, nsteps_s = steps.split(',')
                nsteps = int(nsteps_s)
                self._step_array = [SingleStep(step) for x in range(nsteps)]
            except ValueError as e:
                raise CdsutilsError("Invalid steps description.")
        else:
            try:
                self._step_array = [SingleStep(steps)]
            except ValueError as e:
                raise CdsutilsError("Invalid step description.")

        self._step_count = 0
        self._last_value = None
        self._next_time = None
        self._done = False

    __init__.__doc__ = """
'ezca' is initialized ezca object.

{}
'time_step' specifies time between steps in seconds (default: {})
    """.format(description_common, DEFAULT_TIME_STEP)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s(%s, '%s', '%s')" % (self.__class__.__name__, self._ezca, self._channel, self._steps)

    def step(self):
        """Take next step if alloted time has past.

        If it's time for the next step, the new value is calculated
        and the step channel is updated.  Returns True if done
        stepping.  If all steps have been taken, immediately returns
        True.

        """
        if self._done:
            return True

        current_time = time.time()
        current_value = self._ezca.read(self._channel, use_monitor=False)

        # if this is the first step, populate the variables to be
        # tracked.
        if self._next_time is None:
            # use_monitor=False to force getting the most recent value
            self._last_value = current_value
            self._next_time = current_time + self._time_step

        # if it's not time for the next step, return False
        if current_time < self._next_time:
            return False

        # throw an exception if current value does not equal last
        # value, indicating that the channel is changing underneath us
        if current_value != self._last_value:
            raise CdsutilsError("Channel {} changed during step: {} != {}".format(self._channel, current_value, self._last_value))

        self._last_value = self._step_array[self._step_count](self._last_value)

        # update the channel
        self._ezca[self._channel] = self._last_value

        self._step_count += 1
        self._next_time += self._time_step

        if self._step_count >= len(self._step_array):
            self._done = True
            return True

        return False

##################################################

def step(ezca, *args, **kwargs):
    csteps = []
    for channel, steps in zip(args[0::2], args[1::2]):
        csteps.append(Step(ezca, channel, steps, **kwargs))
    while True:
        ret = []
        for cstep in csteps:
            ret.append(cstep.step())
        if all(ret):
            break
        time.sleep(float(kwargs.get('time_step', DEFAULT_TIME_STEP))/10)

step.__doc__ = """{}

'ezca' is initialized ezca object.

*args is an arbitrary number of channel/steps pairs, where
{}
The 'time_step' kwarg can be used to specify a time_step value (default: {})

Example to increase GAIN1 10 times by one, while simultaneously
decreasing GAIN2 5 times by 3db:

>>> step(ezca, 'GAIN1', '+1,10', 'GAIN2', '-3db,5')

Example to increase OFFSET 5 times by 0.1, once per second:

>>> step(ezca, 'OFFSET', '+0.1,5', time_step=1.0)
""".format(summary, description_common, DEFAULT_TIME_STEP)

##################################################

def main():
    cdesc = summary + "\n\n" + description_common + """
Use '--' to separate optional and required arguments when necessary
(e.g. when <step_spec> is negative)."""

    parser = argparse.ArgumentParser(
        description=cdesc,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-s', '--time-step', metavar='time_step', type=float, default=DEFAULT_TIME_STEP,
        help="time in seconds between steps")
    parser.add_argument(
        'args', metavar='channel steps', nargs='*',
        help="channel/steps pairs")
    args = parser.parse_args()

    # collect channels
    if len(args.args[0::2]) != len(args.args[1::2]):
        raise CliError("must specify step for each channel.")

    arg_list = []
    for channel, steps in zip(args.args[0::2], args.args[1::2]):
        __, channel = split_channel_ifo(channel)
        arg_list += [channel, steps]

    try:
        step(Ezca(), *arg_list, time_step=args.time_step)
    except CdsutilsError as e:
        raise CliError(e)
