import sys
import time
import argparse
import threading
from math import log, exp, pi

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)

from . import nds


class MainLoopThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loop = GObject.MainLoop()
        self.daemon = True
        self.keep_running = True

    def run(self):
        try:
            self.loop.run()
        except KeyboardInterrupt:
            self.loop.quit()
            self.keep_running = False


def audio(channel, filt=None, fixed_gain=None, pan=0.0, agc_setpt=0.2, agc_ugf=1):
    """play NDS channel as audio stream

Produces a real-time audio stream of an NDS testpoint channel.

If no fixed_gain argument is provided, a logarithmic auto gain control
(AGC) will be used.  Otherwise, fixed_gain should be a float that will
used to scale the signal amplitude.

    """

    # FIXME: we have to import foton here, inside the
    # function, because it somehow captures argv and does its own
    # argument parsing, which interferes with any CLI argparse.
    # Should figure out another way around this issue.
    from foton import Filter, FilterDesign

    player = Gst.parse_launch('appsrc name=src ! queue ! audioconvert ! audioresample ! audiopanorama name=pano ! autoaudiosink')
    src = player.get_by_name('src')
    src.set_property('do-timestamp', True)
    src.set_property('is-live', True)
    src.set_property('format', Gst.Format.TIME)
    pano = player.get_by_name('pano')
    pano.set_property('panorama', pan)
    loop_thread = MainLoopThread()
    loop_thread.start()

    first_run = True
    conn = nds.connection()
    print("playing {} (C-c to exit)...".format(channel), file=sys.stderr)
    iterate_args = [[channel,]]
    if conn.get_protocol() == 1:
        iterate_args = [-1, [channel,]]
    for bufs in conn.iterate(*iterate_args):
        samples = bufs[0].data
        sample_rate = bufs[0].channel.sample_rate
        if first_run:
            caps = Gst.caps_from_string('audio/x-raw,format=S16LE,rate=%i,channels=1,layout=interleaved' % sample_rate)
            src.set_property('caps', caps)
        if filt:
            if first_run:
                filt = Filter(FilterDesign(filt, rate=sample_rate))
            samples = filt.apply(samples)
        if fixed_gain:
            # fixed gain
            samples *= 2**15*fixed_gain
        else:
            # logarithmic AGC
            lim = 1e-18
            if first_run:
                agc = log(2**15*agc_setpt) - log(max(max(abs(samples)), lim))
            for n in range(samples.size):
                samples[n] *= exp(agc)
                err = log(2**15*agc_setpt) - log(max(abs(samples[n]), lim))
                agc += 2*pi*agc_ugf*err/sample_rate
                agc = min(max(agc, log(lim)), -log(lim))
        buf = Gst.Buffer.new_wrapped(samples.astype('int16').tobytes())
        src.emit('push-buffer', buf)
        if first_run:
            # fill up the queue in case of network glitches
            time.sleep(samples.size/float(sample_rate))
            player.set_state(Gst.State.PLAYING)
            first_run = False
        if not loop_thread.keep_running:
            break

##################################################

# a summary used by main CLI
summary = audio.__doc__.splitlines()[0]

def main():
    parser = argparse.ArgumentParser(
        description=audio.__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'channel', type=str,
        help="channel to play")
    parser.add_argument(
        '-f', '--filt', type=str, default='',
        help="foton design string for filter to apply to audio stream")
    parser.add_argument(
        '-g', '--fixed-gain', type=float,
        help="use fixed gain")
    parser.add_argument(
        '-p', '--pan', type=float, default=0.0,
        help="position in stereo panorama (-1.0 left -> 1.0 right)")
    parser.add_argument(
        '--agc-setpt', type=float, default=0.2,
        help="setpoint for auto gain control servo (as fraction of full scale)")
    parser.add_argument(
        '--agc-ugf', type=float, default=1,
        help="UGF for auto gain control servo")
    args = parser.parse_args()

    audio(channel=args.channel,
          filt=args.filt,
          fixed_gain=args.fixed_gain,
          pan=args.pan,
          agc_setpt=args.agc_setpt,
          agc_ugf=args.agc_ugf
          )
