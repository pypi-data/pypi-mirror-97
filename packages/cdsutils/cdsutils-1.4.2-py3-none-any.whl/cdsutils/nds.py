import os
import sys
import nds2

from ._util import split_channel_ifo

##################################################

IFO = os.getenv('IFO')

def _args_channel_normalize_ifo(args):
    # this finds a channel list in the supplied argument tuple, and
    # normalize channels names therein.  the channel list is modified
    # in place, so that args argument will be modified after this call
    # is complete, without having to return a new argument tuple.
    nargs = ()
    for arg in args:
        # we assume that any list argument is a channel list
        if type(arg) is list:
            channels = []
            for ci, chan in enumerate(arg):
                __, rest = split_channel_ifo(chan)
                channels += ['%s:%s' % (IFO, rest)]
            nargs += (channels,)
        else:
            nargs += (arg,)
    return nargs


def get_hostport(hostport):
    """Split NDS host:port specification into (host, port)"""
    # default port
    port = 31200
    hostport = hostport.split(':')
    host = hostport[0]
    if len(hostport) > 1:
        port = int(hostport[1])
    return host, port

##################################################

class NDSError(Exception):
    pass


class NDSConnectError(Exception):
    pass


class connection(nds2.connection):
    """CDS NDS2 connection object.

    Unlike the normal nds2.connection object, no arguments need be
    specified in which case the NDSSERVER env var will be used to find
    the best NDS server.

    Also, any channel may be specified without leading IFO: prefix.

    """
    def __init__(self, *args):
        if args:
            return super(connection, self).__init__(*args)

        try:
            serverspec = os.environ['NDSSERVER']
        except KeyError:
            raise NDSError("host:port not specified in NDSSERVER environment variable.")

        if not IFO:
            raise NDSError("IFO environment variable not specified.")

        servers = serverspec.split(',')

        for server in servers:
            try:
                host, port = get_hostport(server)
            except:
                NDSError("NDSSERVER variable incorrectly defined.")

            try:
                return super(connection, self).__init__(host, port)
            except RuntimeError as e:
                if 'SASL' in str(e):
                    raise NDSConnectError("Authentication error.  Check kerberos token (kinit).")
                else:
                    pass

        raise NDSConnectError("Could not connect to any server.")

    #####
    # inherited functions with normalized channel names

    def find_channels(self, *args, **kwargs):
        # the first argument is the channel search pattern
        nargs = list(args)
        if args:
            __, rest = split_channel_ifo(args[0])
            nargs[0] = '%s:%s' % (IFO, rest)
        return super(connection, self).find_channels(*nargs, **kwargs)

    def fetch(self, *args, **kwargs):
        # the list argument is the channel list
        nargs = _args_channel_normalize_ifo(args)
        return super(connection, self).fetch(*nargs, **kwargs)

    def iterate(self, *args, **kwargs):
        # the list argument is the channel list
        nargs = _args_channel_normalize_ifo(args)
        return super(connection, self).iterate(*nargs, **kwargs)

# alias for backwards compatibility
get_connection = connection
