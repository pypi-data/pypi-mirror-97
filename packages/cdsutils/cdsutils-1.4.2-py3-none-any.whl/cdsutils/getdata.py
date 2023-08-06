import numpy as np
from gpstime import gpstime

from . import nds

##################################################


class CDSData(object):
    def __init__(self, name, channel, data, start_time, sample_rate):
        self.name = name
        self.channel = channel
        self.data = data
        self.start_time = start_time
        self.sample_rate = sample_rate

    def __repr__(self):
        return "<CDSData %s (GPS start: %s, Fs: %s, %s samples)>" % (self.channel, self.start_time, self.sample_rate, len(self))

    def __len__(self):
        return len(self.data)

    def append(self, data):
        self.data = np.append(self.data, data)


def getdata(channels, duration, start=None):
    """Get <duration> seconds of NDS data.

    If <start> time is not specified, the next <duration> seconds of
    data will be retrieved online.  Only start times in the past may
    be specified.  Duration may be negative and should behave as
    expected.

    If a single channel name is specified, a single CDSData object is
    returned (see below).  If a list of channels is specified a list
    of CDSData objects is returned, ordered as the input list.

    The CDSData objects contain the following attributes:
      channel        full channel name
      start_time     GPS start time of data
      sample_rate    sample rate of data
      data           time series array

    """
    # if channel is single string, convert to list
    if isinstance(channels, str):
        list_out = False
        channels = [channels]
    else:
        list_out = True

    conn = nds.connection()

    duration = int(round(duration))

    if duration < 0:
        duration *= -1
        if not start:
            start = gpstime.now().gps()
        start -= duration

    if start:
        ctime = int(start)
        start = ctime
        finish = start + duration
        args = [start, finish]
        igfirst = False
    else:
        ctime = 0
        finish = duration
        args = []
        igfirst = True
    args.append(channels)

    data = [None]*len(channels)

    for buf in conn.iterate(*args):
        if igfirst:
            igfirst = False
            continue

        for c, chan in enumerate(channels):
            if not data[c]:
                data[c] = CDSData(chan,
                                  buf[c].channel.name,
                                  buf[c].data,
                                  buf[c].gps_seconds,
                                  buf[c].channel.sample_rate)

                # calculate stride
                stride = int(len(buf[0].data) / buf[0].channel.sample_rate)

            else:
                data[c].append(buf[c].data)

        ctime += stride
        # if we're not retrieving online data, the iterator will just
        # give us as much data as requested and then stop iterating.
        # if we're online, we have to keep track of the number of
        # strides and break once enough data has been retrieved.
        if not start and ctime >= finish:
            break

    if list_out:
        return data
    else:
        return data[0]
