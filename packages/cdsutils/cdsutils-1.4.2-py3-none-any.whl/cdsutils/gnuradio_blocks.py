from numpy import float32

from gnuradio import gr, blocks
from gnuradio.filter import iir_filter_ffd
from gnuradio.gr import threading

from foton import FilterDesign, iir2z

from . import nds


class daq_source_f(gr.hier_block2):
    def __init__(self, channel=None, msgq_limit=2):
        gr.hier_block2.__init__(self, "daq_source_f",
                                gr.io_signature(0, 0, 0),
                                gr.io_signature(1, 1, gr.sizeof_float))
        message_source = blocks.message_source(gr.sizeof_float, msgq_limit)
        self._msgq = message_source.msgq()
        self.connect(message_source, self)
        self.set_channel(channel)

    def set_channel(self, channel):
        if not channel:
            return
        if hasattr(self, '_daqthread'):
            self._daqthread.keep_running = False
            self._daqthread.join()
        self._daqthread = _daq_watcher_thread(self, channel)
        self.rate = self._daqthread.rate
        self._daqthread.start()

    def push(self, data):
        msg = gr.message_from_string(data.tostring(), 0,
                                     gr.sizeof_float, len(data))
        self._msgq.insert_tail(msg)

    def close(self):
        if hasattr(self, '_daqthread'):
            self._daqthread.keep_running = False
            self._daqthread.join()


class _daq_watcher_thread(threading.Thread):
    def __init__(self, source_block, channel, fast=True):
        super.__init__()
        self.setDaemon(True)
        self.source_block = source_block
        self.channel = channel
        self.conn = nds.connection()
        self.rate = get_samp_rate(channel)
        self.keep_running = True

    def run(self):
        iterate_args = [[self.channel]]
        if self.conn.get_protocol() == 1:
            iterate_args = [-1, [self.channel]]
        for bufs in self.conn.iterate(*iterate_args):
            if not self.keep_running:
                break
            self.source_block.push(bufs[0].data.astype(float32))
        del self.conn


def get_samp_rate(channel):
    conn = nds.connection()
    try:
        samp_rate = conn.find_channels(channel)[0].sample_rate
    except IndexError:
        raise Exception('Unknown channel %s' % channel)
    return int(samp_rate)


class foton_filter_ff(gr.hier_block2):
    def __init__(self, design="", samp_rate=None):
        gr.hier_block2.__init__(self, "foton_filter_ff",
                                gr.io_signature(1, 1, gr.sizeof_float),
                                gr.io_signature(1, 1, gr.sizeof_float))
        self.rate = samp_rate
        self.set_design(design)

    def set_design(self, design):
        filt = FilterDesign(design, rate=self.rate)
        coeffs = iir2z(filt)
        gain = coeffs[0]
        coeffs_by_sos = [coeffs[n:n+4] for n in range(1, len(coeffs[1:]), 4)]
        sections = [self, blocks.multiply_const_ff(gain)]
        for (b1, b2, a1, a2) in coeffs_by_sos:
            ff_taps = (1.0, b1, b2)
            fb_taps = (1.0, -a1, -a2)
            sections.append(iir_filter_ffd(ff_taps, fb_taps))
        sections.append(self)
        self.connect(*sections)


if __name__ == '__main__':
    import wx
    import sys
    from gnuradio.wxgui import scopesink2
    from gnuradio.wxgui import stdgui2
    test_chan = sys.argv[1]

    class top_block(stdgui2.std_top_block):
        def __init__(self, frame, panel, vbox, argv):
            stdgui2.std_top_block.__init__(self, frame, panel, vbox, argv)
            frame_decim = 1
            v_scale = None
            t_scale = 0.00003
            src = daq_source_f(test_chan)
            scope = scopesink2.scope_sink_f(panel, test_chan,
                                            sample_rate=src.rate,
                                            frame_decim=frame_decim,
                                            v_scale=v_scale,
                                            t_scale=t_scale)
            vbox.Add(scope.win, 1, wx.EXPAND)
            self.connect(src, scope)

    app = stdgui2.stdapp(top_block, test_chan)
    app.MainLoop()
