##################################################
# Gnuradio Python Flow Graph
# Title: Water - channel
# Author: ccw
# Description: Live waterfall plotter for LIGO data
# Generated: Wed Feb  5 15:45:54 2014
##################################################

import os
import sys
import ctypes
import argparse

import sip
from PyQt5 import Qt
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes

from . import gnuradio_blocks


class Water(gr.top_block, Qt.QWidget):
    def __init__(self, channel="None", samp_rate=None, res=1, bw=None):
        gr.top_block.__init__(self, "Water - " + channel)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Water - " + channel)
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Water")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.channel = channel
        self.samp_rate = samp_rate
        self.res = res
        self.bw = bw

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_sink_x_0 = qtgui.sink_f(
            int(samp_rate/res),  # fftsize
            firdes.WIN_HANN,  # wintype
            0,  # fc
            bw,  # bw
            "QT GUI Plot",  # name
            False,  # plotfreq
            True,  # plotwaterfall
            False,  # plottime
            False,  # plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/res)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.ligocds_daq_source_f_0 = gnuradio_blocks.daq_source_f(channel)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.ligocds_daq_source_f_0, 0), (self.qtgui_sink_x_0, 0))

    # QT sink close method reimplementation
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Water")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel
        self.ligocds_daq_source_f_0.set_channel(self.channel)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_res(self):
        return self.res

    def set_res(self, res):
        self.res = res

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.qtgui_sink_x_0.set_frequency_range(0, self.bw)


summary = """waterfall plot of NDS channel"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'channel', type=str,
        help="channel")
    parser.add_argument(
        '-r', '--res', type=float, default=1,
        help="Set res [default={}]".format(1))
    parser.add_argument(
        '-b', '--bw', dest='bw', type=float, default=None,
        help="Set bw")
    args = parser.parse_args()

    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()", file=sys.stderr)

    #if gr.enable_realtime_scheduling() != gr.RT_OK:
    #    print "Error: failed to enable realtime scheduling."
    qapp = Qt.QApplication(sys.argv)

    samp_rate = gnuradio_blocks.get_samp_rate(args.channel)
    if args.bw is None:
        args.bw = samp_rate
    tb = Water(channel=args.channel, samp_rate=samp_rate, res=args.res, bw=args.bw)
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    # to clean up Qt widgets
    tb = None
