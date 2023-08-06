import argparse

import ezca
from ezca.const import BUTTONS_ORDERED

from ._util import split_channel_ifo


description = """read/switch buttons in filter module

The first argument is the base filter name (minus trailing
switch/button identifiers).  If no other arguments are given, the list
of engaged buttons in the filter will be dumped to stdout.

Otherwise, the remaining arguments are interpreted as buttons/action
sequences (e.g "INPUT OUTPUT ON").  Multiple buttons/action sequences
may be specified.

buttons:
    INPUT | IN
    OFFSET
    FM1, FM2, ..., FM10
    LIMIT
    OUTPUT | OUT
    DECIMATION | DECIMATE
    HOLD
    FMALL
    ALL

actions:
    ON
    OFF
"""
summary = description.splitlines()[0]
usage = 'switch [-h] <filter> [<button> [<button>...] <action> ...]'


def main():
    parser = argparse.ArgumentParser(
        usage=usage,
        description=description.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filter', type=str,
        help=argparse.SUPPRESS)
    parser.add_argument(
        'buttons_and_actions', nargs=argparse.REMAINDER,
        help=argparse.SUPPRESS)
    args = parser.parse_args()

    __, channel = split_channel_ifo(args.filter)

    try:
        e = ezca.Ezca()
        if args.buttons_and_actions:
            e.switch(channel, *args.buttons_and_actions)
        else:
            buttons = e.get_LIGOFilter(channel).get_current_switch_mask().buttons
            for button in BUTTONS_ORDERED:
                if button in buttons:
                    print(button)
    except ezca.EzcaError as e:
        raise SystemExit(e)
    except ezca.ligofilter.LIGOFilterError as e:
        raise SystemExit(e)
