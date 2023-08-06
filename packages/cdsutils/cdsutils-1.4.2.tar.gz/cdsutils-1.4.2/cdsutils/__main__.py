import os
import sys
import signal
import importlib

from .__init__ import __version__, CMDS


sys.path.insert(0, os.path.dirname(__file__))

PROG = 'cdsutils'


def usage():
    print('''usage: {} <cmd> <args>

Advanced LIGO Control Room Utilites

Available commands:
'''.format(PROG))
    for cmd in CMDS:
        try:
            mod = importlib.import_module('.'+cmd, package='cdsutils')
            summary = mod.summary
        except ImportError as e:
            summary = 'NOT SUPPORTED: ' + str(e)
        print('  {0:<12s} {1}'.format(cmd, summary))
    print()
    print('  {0:<12s} {1}'.format('version', 'print version info and exit'))
    print('  {0:<12s} {1}'.format('help', 'this help'))
    print('''
Add '-h' after individual commands for command help.''')

def main():
    if len(sys.argv) == 1:
        usage()
        sys.exit()

    if sys.argv[1] in ['help','-h','--help']:
        usage()
        sys.exit()

    if sys.argv[1] in ['version','-v','--version']:
        print('cdsutils', __version__)
        sys.exit()

    if sys.argv[1] not in CMDS:
        print("Unknown command: {}".format(sys.argv[1]), file=sys.stderr)
        print("Type '{} help' for more info.".format(PROG), file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    # handle Ctrl-C
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # module import execution for commands
    sys.argv = sys.argv[1:]
    try:
        mod = importlib.import_module('.'+cmd, package='cdsutils')
    except ImportError as e:
        raise SystemExit("Command '{}' not supported: {}".format(cmd, e))
    try:
        mod.main()
    except KeyboardInterrupt:
        raise SystemExit()


if __name__ == '__main__':
    main()
