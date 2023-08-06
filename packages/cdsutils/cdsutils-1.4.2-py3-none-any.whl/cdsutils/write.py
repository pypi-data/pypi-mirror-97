import argparse

from ezca import Ezca, EzcaError

from ._util import split_channel_ifo


description = """write EPICS channel value
"""
summary = description.splitlines()[0]


def main():
    parser = argparse.ArgumentParser(
        description=description.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'chanvals', metavar='channel value', nargs='+',
        help="channel/value pairs")
    args = parser.parse_args()

    ezca = Ezca()
    for channel, value in zip(args.chanvals[0::2], args.chanvals[1::2]):
        try:
            __, channel = split_channel_ifo(channel)
            print(ezca.write(channel, value))
        except EzcaError as e:
            raise SystemExit(e)
