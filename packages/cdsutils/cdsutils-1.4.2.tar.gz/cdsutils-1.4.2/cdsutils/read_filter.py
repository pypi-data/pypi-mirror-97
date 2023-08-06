import os
import argparse
import operator
import functools

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

import ezca
# FIXME: root steals command line arguments, so we have to import
# foton opportunistically
import foton
import gpstime

from ._util import split_channel_ifo


USERAPPS = os.getenv(
    'USERAPPS_DIR',
    '/opt/rtcds/userapps/release',
)
FILTER_FILE_PATH = os.getenv(
    'FILTER_FILE_PATH',
    os.path.join(USERAPPS, 'isi/m1/filterfiles'),
)


def foton_retrieve_filter(filter_name):
    """retrieve the foton filter for the specified SFM channel

    Finds the corresponding filter file in USERAPPS/*/filterfiles,
    loads the files with foton, and extracts the appropriate filter
    bank.

    """
    IFO, rest = split_channel_ifo(filter_name)
    subsys, fname = rest.split('-', 1)
    instance, rest = fname.split('_', 1)
    filterfile = f'{IFO}{subsys}{instance}'.upper() + '.txt'
    path = os.path.join(
        USERAPPS,
        subsys.lower(),
        IFO.lower(),
        'filterfiles',
        filterfile,
    )
    if not os.path.exists(path):
        raise FileNotFoundError(f"filter file not found: {path}")
    import foton
    ff = foton.FilterFile(path)
    return ff[fname]


def sfm_retrieve_state(filter_name, gps=None):
    """Retrieve the state of a filter module

    If a GPS time is not provided, the current state will be retrieved
    via EPICS.  If a time is provided, NDS will be used to retrieve
    the state from that time.  A list of all active buttons for the
    filter will be returned.

    """
    if gps:
        import nds2
        os.environ['NDSSERVER'] = 'nds.ligo-wa.caltech.edu'
        buf = nds2.fetch([filter_name+'_SWSTAT'], int(gps), int(gps+1))
        state = int(buf[0].data[0])
        mask = ezca.SFMask.from_swstat(state)
        buttons = [button for button in ezca.const.BUTTONS_ORDERED if button in mask]
    else:
        ligo_filter = ezca.Ezca().LIGOFilter(filter_name)
        buttons = ligo_filter.get_current_switch_mask().buttons
    return buttons


class FilterState:
    def __init__(self, ff, engaged=False):
        self.ff = ff
        self.engaged = engaged

    @property
    def name(self):
        """Filter name"""
        return self.ff.name

    def freqresp(self, freq):
        """Filter frequency response at `freq`"""
        import foton
        num, den, gain = foton.iir2poly(self.ff)
        w, fr = signal.freqs(
            gain*np.array(num),
            np.array(den),
            worN=2*np.pi*freq,
        )
        return fr


def sfm_fetch(filter_name, gps=None):
    """fetch all filters for the specified SFM

    Returns a list of FilterState objects.

    """
    if gps is not None:
        if gps == 'now':
            gps = None
        buttons = sfm_retrieve_state(filter_name, gps=gps)
    else:
        buttons = []
    #engaged = list(map(lambda b: int(b[2]), filter(lambda b: '_ENGAGED' in b, buttons)))
    engaged = list(map(lambda b: int(b[2]), filter(lambda b: b[:2] == 'FM', buttons)))
    ff = foton_retrieve_filter(filter_name)
    ffs = [FilterState(f, i+1 in engaged) for i, f in enumerate(ff)]
    return ffs



def bode(fig, freq, fr, label=None, **kwargs):
    """bode plot of frequency response

    """
    ax1, ax2 = fig.axes
    mag = 20 * np.log10(np.abs(fr))
    ang = np.angle(fr) * 180/np.pi
    ax1.semilogx(freq, mag, label=label, **kwargs)
    ax2.semilogx(freq, ang, **kwargs)


def plot_bank(freq, ffs, title=None):
    """bode plot of SFM filter bank state

    Takes list of FilterState objects.  All "engaged" filters will be
    convolved and the total frequency response will be included.

    """
    frs = {ff.name: ff.freqresp(freq) for ff in ffs}

    fig, (ax1, ax2) = plt.subplots(2, 1)

    frs_engaged = [frs[ff.name] for ff in ffs if ff.engaged]
    if frs_engaged:
        fr_total = functools.reduce(
            operator.mul,
            frs_engaged,
        )
        bode(fig, freq, fr_total, color='black', linestyle='-', linewidth=4, alpha=0.7)

    for i, ff in enumerate(ffs):
        ii = i+1
        label = f'FM{ii}: {ff.name}'
        fr = frs[ff.name]
        if ff.engaged:
            style = '-'
            linewidth = 3
        else:
            style = '--'
            linewidth = 2
        bode(fig, freq, fr, label=label, linestyle=style, linewidth=linewidth, alpha=0.7)

    # ax1.set_xticklabels([])
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_ylabel('magnitude [dB]')
    ax2.set_ylabel('phase [degrees]')
    ax2.set_xlabel('frequency [Hz]')
    ax1.legend(ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.2))
    plt.suptitle(title)
    plt.show()


parser = argparse.ArgumentParser()
parser.add_argument(
    'fname',
    help='filter name',
)
parser.add_argument(
    'time', nargs='?',
    help='absolute or relative date/time string (accepts GPS)',
)


def main():
    args = parser.parse_args()

    if args.time:
        args.time = gpstime.parse(args.time).gps()

    ffs = sfm_fetch(args.fname, gps=args.time)

    freq = np.logspace(-3, 3, 1000)

    plot_bank(freq, ffs, title=args.fname)


if __name__ == '__main__':
    main()
