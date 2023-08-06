import argparse
import numpy as np
from gpstime import gpstime

from . import nds


def calc_std(stddev):
    return bool(stddev)


def avg(seconds, channels, stddev=False):
    """average one or more NDS channels

    'seconds' is amount of time to average.  If negative, past data
    will be used.

    If 'channels' is a single channel name string, then a single value
    (tuple) will be returned.  If a list of channels is specified, the
    output will be a list of values (tuples).

    If 'stddev' is True or 1 or 2, the stddev will be calculated as
    well and the return value for each channel will be a tuple.  When
    specified as 2, the divide by N method will be used.

    """
    # if channel is single string, convert to list
    if isinstance(channels, str):
        list_out = False
        channels = [channels]
    else:
        list_out = True

    conn = nds.connection()

    # default for online data
    stride = 1

    if seconds < 0:
        # past data request
        seconds = abs(seconds)
        stop = int(gpstime.tconvert().gps())
        start = int(stop - seconds)
        args = [start, stop]
        igfirst = False
    else:
        # live data request
        args = []
        igfirst = True
    args += [stride]
    args += [channels]

    # the "delta degree of freedom" compensator for the stddev
    # calculation is given by the value of the stddev argument
    if calc_std(stddev):
        if stddev is True:
            ddof = 1
        else:
            ddof = stddev

    # initial values
    N = [0]*len(channels)
    mean = [0]*len(channels)
    if calc_std(stddev):
        var = [0]*len(channels)
        std = [0]*len(channels)

    accum = 0
    for buf in conn.iterate(*args):
        if igfirst:
            igfirst = False
            #print >>sys.stderr, "ignoring first online block..."
            continue

        #print >>sys.stderr, "received: %s + %s" % (buf[0].gps_seconds, float(buf[0].length) / buf[0].channel.sample_rate)

        # add stride length to accumulated data time
        accum += stride

        for c, chan in enumerate(channels):
            # if we've got more than the requested number of seconds,
            # find the data point corresponding to the last time
            if accum > seconds:
                last = int(round((accum - seconds) * buf[c].channel.sample_rate))
            else:
                last = len(buf[c].data)

            data = buf[c].data[:last]

            # calculate current "chuck" mean and variance
            cN = len(data)
            cmean = np.mean(data)
            cvar = np.var(data)

            nN = N[c] + cN

            # running "chunk" mean should be fully accurate
            mean[c] = ((mean[c] * N[c]) + (cmean * cN)) / nN

            # running "chunk" variance calculates the variance for
            # each chunk using the chunk mean, as opposed to the
            # running mean.
            # note: ddof is the "delta degree of freedom" compensation
            # to the number of elements
            if calc_std(stddev):
                var[c] = ((var[c] * (N[c] - ddof)) + (cvar * (cN - ddof))) / (nN - ddof)

            # running number of points
            N[c] = nN

        if accum >= seconds:
            break

    # output
    if calc_std(stddev):
        # standard deviation is sqrt of variance
        for c, v in enumerate(var):
            std[c] = var[c]**0.5

        output = list(zip(mean, std))
    else:
        output = mean

    # return
    if list_out:
        return output
    else:
        return output[0]

##################################################

# a summary used by main CLI
summary = avg.__doc__.splitlines()[0]

description = '''

The average for each channel will be printed to stdout.  If either -s
option is provided, the stddev will be calculated as well and will be
returned as a second column in the output.

'seconds' is the amount of time to average.  If positive, data will be
gathered starting at time of execution.  If negative, past data will
be used.

'''

def main():
    parser = argparse.ArgumentParser(
        description=description.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'seconds', type=float,
        help="length of average in seconds (can be negative to use past data)")
    parser.add_argument(
        'channels', type=str, nargs='+',
        help="list of channels to be averaged")
    parser.add_argument(
        '-n', action="store_true",
        help="don't print channel names, just averaged values")
    sgroup = parser.add_mutually_exclusive_group()
    sgroup.add_argument(
        '-s', dest='stddev', action='store_const', const=1,
        help="add standard deviation column, using divide by n-1 samples definition")
    sgroup.add_argument(
        '-s2', dest='stddev', action='store_const', const=2,
        help="add standard deviation column, using divide by n samples definition)")
    args = parser.parse_args()

    data = avg(args.seconds, args.channels, args.stddev)

    for c, chan in enumerate(args.channels):
        out = ''
        if not args.n:
            out += chan + ' '
        if calc_std(args.stddev):
            out += '{} {}'.format(data[c][0], data[c][1])
        else:
            out += '{}'.format(data[c])
        print(out)
