import time
import argparse

import ezca

from .errors import CdsutilsError


WAITTIME = 0.01


def trigservo(
        ezca,
        channel=None,
        readback=None,
        channel2=None,
        gain=1.0,
        gain2=0.0,
        setval=0.0,
        timeout=-1.0,
        triggerChannel=None,
        triggerOn=0,
        triggerOff=None,
        triggerDelay=0,
        triggerGreaterThan=True,
):
    """servo EPICS channel with trigger

    Can handle up to 2 control channels with either common or
    differential actuation.

    """
    if not channel:
        raise CdsutilsError('Servo was not passed a valid control channel.')
    if not setval:
        setval = 0.0

    if timeout == 0:
        return True

    if triggerChannel is None:
        triggerState = None
    else:
        triggerState = 'Off'
    triggerStartTime = None

    if triggerOff is None:
        triggerOff = triggerOn

    # start time
    program_start_time = time.time()
    t0 = time.time()
    t = 0
    prev = 0
    dt = None
    err = None
    ctrl = 1.0
    ctrl2 = 1.0

    ctrl = ezca.read(channel)
    if channel2:
        ctrl2 = ezca.read(channel2)

    while True:
        if not (triggerChannel is None):
            if triggerState == 'Off':
                triggerValue = ezca.read(triggerChannel)
                if triggerGreaterThan:
                    if triggerValue > triggerOn:
                        if triggerStartTime is None:
                            triggerStartTime = time.time()
                        if (time.time() - triggerStartTime) > triggerDelay:
                            triggerState = 'On'
                            triggerStartTime = None
                            ctrl = 1.0
                            ctrl2 = 1.0
                            ctrl = ezca.read(channel)
                            if channel2:
                                ctrl2 = ezca.read(channel2)
                            t = 0
                            prev = 0
                            dt = None
                            err = None
                            t0 = time.time()
                    else:
                        triggerStartTime = None
                # trigger Greater than is false, means less than
                else:
                    if triggerValue < triggerOn:
                        if triggerStartTime is None:
                            triggerStartTime = time.time()
                        if (time.time() - triggerStartTime) > triggerDelay:
                            triggerState = 'On'
                            triggerStartTime = None
                            ctrl = 1.0
                            ctrl2 = 1.0
                            ctrl = ezca.read(channel)
                            if channel2:
                                ctrl2 = ezca.read(channel2)
                            t = 0
                            prev = 0
                            dt = None
                            err = None
                            t0 = time.time()
                    else:
                        triggerStartTime = None
            elif triggerState == 'On':
                triggerValue = ezca.read(triggerChannel)
                if triggerGreaterThan:
                    if triggerValue < triggerOff:
                        triggerState = 'Off'
                        triggerStartTime = None
                #Trigger Greater than is false, means less than
                else:
                    if triggerValue > triggerOff:
                        triggerState = 'Off'
                        triggerStartTime = None

        if (triggerState is None) or (triggerState == 'On'):
            time.sleep(WAITTIME)
            if readback:
                err = float(ezca.read(readback))
            else:
                if (gain2 != None):
                    err = (ctrl + gain2 * ctrl2) / (1 + abs(gain2))
                else:
                    err = ctrl

            err = err - setval
            err = -1*err
            t = time.time() - t0
            dt = t - prev
            prev = t
            # calculate control
            ctrl = ctrl - (gain * dt * err)
            if (gain2 != None):
                ctrl2 = ctrl2 - (gain2 * gain * dt * err)
            if not ((timeout == None) | ((time.time() - program_start_time) < timeout)):
                break
            # set new control value
            ezca.write(channel,ctrl)
            # set new control value on 2nd channel
            if (channel2) and (gain2 != None):
                ezca.write(channel,ctrl)

    return True

##################################################

summary = trigservo.__doc__.splitlines()[0]

def main():
    parser = argparse.ArgumentParser(
        description=trigservo.__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'channel',
        help="control channel")
    parser.add_argument(
        '-r', '--readback',
        help="readback (error) channel")
    parser.add_argument(
        '-c', '--comm',
        help="2nd control channel (common)")
    parser.add_argument(
        '-d', '--diff',
        help="2nd control channel (differential)")
    parser.add_argument(
        '-g', '--gain', type=float,
        help="gain between readback and channel")
    parser.add_argument(
        '-s', '--value', type=float,
        help="set value")
    parser.add_argument(
        '-t', '--duration', type=float,
        help="timeout (sec)")
    parser.add_argument(
        '--trigChan',
        help="Trigger channel to control whether servo is on or off")
    parser.add_argument(
        '--trigOn', type=float,
        help="trigger threshold level to turn on")
    parser.add_argument(
        '--trigOff', type=float,
        help="trigger threshold level to turn off (defaults to trigOn)")
    parser.add_argument(
        '--trigDelay', type=float,
        help="time period to wait while trigger channel is above threshold before transitioning to on or off")
    parser.add_argument(
        '--trigInvert', action="store_true",
        help="flag to have channel go below threshold to turn on")
    args = parser.parse_args()

    if (args.comm and args.diff):
        raise parser.error('Only a single 2nd channel can be set.  Either common or differential, not both.')

    channel2 = None
    gain2 = None
    if args.comm:
        channel2 = str(args.comm)
        gain2 = 1.0
    if args.diff:
        channel2 = str(args.diff)
        gain2 = -1.0

    if args.trigInvert:
        triggerGreaterThan = False
    else:
        triggerGreaterThan = True

    trigservo(ezca.Ezca(),
          args.channel,
          args.readback,
          channel2,
          args.gain,
          gain2,
          args.value,
          args.duration,
          args.trigChan,
          args.trigOn,
          args.trigOff,
          args.trigDelay,
          triggerGreaterThan)
