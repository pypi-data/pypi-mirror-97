import os
import argparse
import operator
import functools

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from ezca import SFMask, Ezca
import ezca.const as ezca_const
# FIXME: root steals command line arguments, so we have to import
# foton opportunistically
#import foton

from ._util import split_channel_ifo


#############################################


USERAPPS = os.getenv(
    'USERAPPS_DIR',
    '/opt/rtcds/userapps/release',
)

#############################################


def foton_find_filter(filter_name):
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


class FilterState:
    def __init__(self, ff, engaged=False):
        self.ff = ff
        self.engaged = engaged

    @property
    def name(self):
        """Filter name"""
        return self.ff.name

    def freqresp(self, freq):
        """Filter frequency response at specified frequencies"""
        import foton
        num, den, gain = foton.iir2poly(self.ff)
        w, fr = signal.freqs(
            gain*np.array(num),
            np.array(den),
            worN=2*np.pi*freq,
        )
        return fr


class FilterModuleState:
    def __init__(self, name, ezca=None):
        """Initialize with the full base channel name of the filter.

        If an Ezca object is supplied it will be used to retrieve the
        current state of the filter module.

        """
        self.fm = foton_find_filter(name)
        self.name = name
        self.ligofilter = None
        if ezca:
            self.ligofilter = ezca.LIGOFilter(name)

    def __getitem__(self, name):
        """get individual filter by index

        Accepts either integer or string number, or 'FM?' string.
        Indicies are 1-indexed.

        """
        try:
            i = int(name)
        except ValueError:
            # assume name is string 'FM?' or '?'
            i = int(name[-1])
            if i == 0:
                i = 10
        assert i in range(1, 11)
        if self.ligofilter:
            engaged = self.ligofilter.is_engaged(f'FM{i}')
        else:
            engaged = False
        return FilterState(self.fm[i-1], engaged)

    def __iter__(self):
        return iter([self[i] for i in range(1, 11)])

    def freqresp(self, freq):
        """full module frequency response at the specified frequencies

        Convolves the response of all engaged filters.

        """
        return functools.reduce(
            operator.mul,
            [f.freqresp(freq) for f in self if f.engaged]
        )


def bode(fig, freq, fr, label=None, **kwargs):
    """bode plot of frequency response

    """
    ax1, ax2 = fig.axes
    mag = 20 * np.log10(np.abs(fr))
    ang = np.angle(fr) * 180/np.pi
    line, = ax1.semilogx(freq, mag, label=label, **kwargs)
    ax2.semilogx(freq, ang, **kwargs)
    return line


def plot_sfm(freq, fms):
    """bode plot state of CDS standard filter module (SFM)

    Takes a FilterModuleState object.  All "engaged" filters will be
    convolved and the total frequency response will be included.

    """
    frs = {ff.name: ff.freqresp(freq) for ff in fms}

    fig, (ax1, ax2) = plt.subplots(2, 1)

    frs_engaged = [frs[ff.name] for ff in fms if ff.engaged]
    if frs_engaged:
        fr_total = functools.reduce(
            operator.mul,
            frs_engaged,
        )
        linet = bode(fig, freq, fr_total, label='Total', color='black', linestyle='-', linewidth=5, alpha=0.7)
        ax1.add_artist(ax1.legend(handles=[linet], loc='upper right'))

    lines = []
    for i, ff in enumerate(fms):
        ii = i+1
        label = f'FM{ii}: {ff.name}'
        fr = frs[ff.name]
        if ff.engaged:
            style = '-'
            linewidth = 3
        else:
            style = '--'
            linewidth = 2
        lines.append(bode(fig, freq, fr, label=label, linestyle=style, linewidth=linewidth, alpha=0.7))

    ax1.legend(handles=lines, ncol=5, loc='upper center', bbox_to_anchor=(0.5, 1.2))

    # ax1.set_xticklabels([])
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_ylabel('magnitude [dB]')
    ax2.set_ylabel('phase [degrees]')
    ax2.set_xlabel('frequency [Hz]')
    plt.suptitle(f"{fms.name} (solid lines: engaged filters)")
    plt.show()

#############################################


def cmd_decode(args):
    if len(args.SW) == 1:
        sw = args.SW[0]
        try:
            SWSTAT = int(sw)
        except ValueError:
            SWSTAT = Ezca().read(sw)
        buttons = SFMask.from_swstat(SWSTAT)
    elif len(args.SW) == 2:
        try:
            SW1 = int(args.SW[0])
            SW2 = int(args.SW[1])
        except ValueError:
            raise SystemExit("SW values must be integers")
        buttons = SFMask.from_sw(SW1, SW2).buttons
    else:
        raise SystemExit("Improper number of arguments.")

    for button in ezca_const.BUTTONS_ORDERED:
        if button in buttons:
            print(button)


def cmd_encode(args):
    BUTTONS = [b.upper() for b in args.BUTTONS]
    try:
        mask = SFMask.for_buttons_engaged(*BUTTONS, engaged=args.engaged)
    except Exception as e:
        raise SystemExit("Error: "+str(e))
    print('SW1: {:d}'.format(mask.SW1))
    print('SW2: {:d}'.format(mask.SW2))
    print('SWSTAT: {:d}'.format(mask.SWSTAT))


def cmd_show(args):
    ezca = None
    if args.epics:
        ezca = Ezca()
    fms = FilterModuleState(args.FILTER, ezca=ezca)
    freq = np.logspace(-3, 3, 1000)
    plot_sfm(freq, fms)


summary = "decode/encode filter module switch values"


def main():
    parser = argparse.ArgumentParser(
        description=summary,
    )
    subparsers = parser.add_subparsers()
    parser_decode = subparsers.add_parser('decode', help="decode SFM state")
    parser_decode.set_defaults(func=cmd_decode)
    parser_decode.add_argument(
        'SW', metavar='FILTER/SW', nargs='+',
        help="filter name (for EPICS state retrieval), integer SWSTAT value, or integer SW1/2 values"
    )
    parser_encode = subparsers.add_parser('encode', prefix_chars='-+', help="encode SFM state")
    parser_encode.set_defaults(func=cmd_encode)
    parser_encode.add_argument(
        '+engaged', '+e', action='store_false',
        help="don't include engaged button bits"
    )
    parser_encode.add_argument(
        'BUTTONS', nargs='+',
        help="button name list"
    )
    parser_show = subparsers.add_parser('show', prefix_chars='-+', help="bode plot of SFM state")
    parser_show.set_defaults(func=cmd_show)
    parser_show.add_argument(
        'FILTER',
        help="filter name"
    )
    parser_show.add_argument(
        '+epics', '+e', action='store_false',
        help="don't fetch current state via EPICS"
    )
    args = parser.parse_args()
    args.func(args)
