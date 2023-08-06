import argparse

from ezca import Ezca, EzcaError

from ._util import split_channel_ifo


summary = "read EPICS channel value"


def main():
    parser = argparse.ArgumentParser(
        description=summary,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'channel', type=str, nargs='+',
        help="channel name")
    parser.add_argument(
        '-S', dest="as_string", action="store_true",
        help="retrieve value as string")
    args = parser.parse_args()

    if isinstance(args.channel, str):
        channels = [args.channel]
    else:
        channels = args.channel

    ezca = Ezca()
    for channel in channels:
        try:
            __, channel = split_channel_ifo(channel)
            print(ezca.read(channel, as_string=args.as_string))
        except EzcaError as e:
            raise SystemExit(e)
