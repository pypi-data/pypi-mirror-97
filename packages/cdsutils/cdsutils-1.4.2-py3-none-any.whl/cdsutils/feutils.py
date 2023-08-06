from __future__ import print_function
import os
import re
import time

##########

IFO = os.getenv('IFO')
SITE = os.getenv('SITE')
if not IFO:
    raise ImportError("could not find IFO environment variable.")
if not SITE:
    raise ImportError("could not find SITE environment variable.")

RTCDS = '/opt/rtcds/{site}/{ifo}'.format(site=SITE.lower(), ifo=IFO.lower())
if IFO == 'H1':
    DAQ = 'h1dc0'
elif IFO == 'L1':
    DAQ = 'l1daqdc0'
MASTER = os.path.join(RTCDS, 'target', DAQ, 'master')

FEC_DCUID_RE = re.compile('{IFO}:FEC-([^_]*)_CPU_METER.HIGH'.format(IFO=IFO))
MODEL_RE = re.compile('{}(.*)'.format(IFO.lower()))

##########

def _get_dcuid_autoburt(name):
    """Find model DCUID by scanning for channel in model autoBurt.req

    The DCUID is determiend by parsing a FEC channel from the file.

    """
    fullname = '{}{}'.format(IFO.lower(), name)
    path = '{rtcds}/target/{model}/{model}epics/autoBurt.req'.format(rtcds=RTCDS, model=fullname)
    try:
        with open(path) as f:
            for chan in f:
                dcuid_match = FEC_DCUID_RE.match(chan)
                if dcuid_match:
                    return int(dcuid_match.group(1))
    except IOError:
        pass


def _get_models_autoburt():
    """Generator of model (name, dcuid) tuples from autoBurt.req files

    Finds all model autoBurt.req files, and scans those for DCUIDs.

    """
    # Make a list of all of the possible FEs by looking through
    # the target dir for files matching model pattern
    for model in os.listdir('{}/target/'.format(RTCDS)):
        name_match = MODEL_RE.match(model)
        if not name_match:
            continue
        name = name_match.group(1)
        dcuid = _get_dcuid_autoburt(name)
        if dcuid:
            yield name, dcuid


def _get_models_ini_master():
    """Generator over model (name, inifile) tuples from ini files in DAQ master.

    """
    re_ss = re.compile('{rtcds}/chans/daq/{IFO}(.*).ini'.format(rtcds=RTCDS, IFO=IFO))
    with open(MASTER) as f:
        for ini in f:
            ini = ini.strip()
            match = re_ss.match(ini)
            if match:
                model = match.group(1).lower()
                yield model, ini


def _get_models_dcuid_master():
    """Generator over model (name, dcuid) tuples from ini files.

    """
    re_fec = re.compile('\[.*:FEC-(.*)_CPU_METER\]')
    for (model, ini) in get_active_model_ini():
        with open(ini) as f:
            for line in f:
                g = re_fec.search(line)
                if g:
                    dcuid = int(g.group(1))
                    yield model, dcuid


def _get_dcuid_ezca(name):
    """Return DCUID for given model name by channel access.

    """
    sys = name[2:5].upper()
    rest = name[5:].upper()
    if rest:
        prefix = '%s-%s_' % (sys, rest)
    else:
        prefix = '%s-' % (sys)
    chan = '%sDCU_ID' % (prefix)
    return int(ezca[chan])

##########

class CDSFrontEnd(object):
    """Interface to CDS Front End model.

    """
    def __init__(self, name, dcuid):
        """Initalize with the model name and dcuid.

        Name should be without leading <ifo> prefix:

        e.g. 'lsc', 'susetmx', etc.

        """
        self.__ifo = IFO.lower()
        self.__name = name.lower()
        self.__DCUID = int(dcuid)

    @classmethod
    def find(cls, uid):
        """Retrieve CDSFrontEndModel by name or dcuid."""
        name = None
        dcuid = None
        try:
            dcuid = int(uid)
        except ValueError:
            try:
                name = uid.lower()
            except AttributeError:
                raise ValueError("could not parse model: {}".format(uid))
        if name:
            dcuid = _get_dcuid_autoburt(name)
            return cls(name, dcuid)
        # as last resort, find model/dcuid by scanning all available models
        for n, d in _get_models_autoburt():
            if n == name or d == dcuid:
                name = n
                dcuid = d
                return cls(name, dcuid)
        raise ValueError("could not find model: {}".format(uid))

    @property
    def name(self):
        """Model abbreviated name."""
        return self.__name

    @property
    def fullname(self):
        """Model full name."""
        return '%s%s' % (self.__ifo, self.__name)

    @property
    def DCUID(self):
        """Model DCUID."""
        return self.__DCUID
    FEC = DCUID
    dcuid = DCUID
    fec = DCUID

    @property
    def pseudo(self):
        return self.dcuid > 1023

    def __str__(self):
        pseudo_flag = ''
        if self.pseudo:
            pseudo_flag = 'PSEUDO'
        return "<{} '{}' (dcuid: {}) {}>".format(
            self.__class__.__name__,
            self.name,
            self.dcuid,
            pseudo_flag,
        )

    def __fec_chan(self, chan):
        return 'FEC-%d_%s' % (self.dcuid, chan)

    def __getitem__(self, chan):
        """Get FEC channel value."""
        return ezca[self.__fec_chan(chan)]

    def __setitem__(self, chan, value):
        """Set FEC channel value"""
        ezca[self.__fec_chan(chan)] = value

    ##########
    # SDF

    @property
    def SDF_DIFF_CNT(self):
        return int(self['SDF_DIFF_CNT'])

    def load_snap(self, snap):
        """Load the specified snap file.
        
        """
        log("SDF LOAD: %s: '%s'" % (self.name, snap))
        self['SDF_NAME'] = snap
        time.sleep(0.1)
        self['SDF_RELOAD'] = 1

    def sdf_get_request(self):
        """Get requested SDF snap file."""
        return self['SDF_NAME']

    def sdf_get_loaded_table(self):
        """Get SDF snap currently loaded to TABLE."""
        return self['SDF_LOADED']

    def sdf_get_loaded_edb(self):
        """Get SDF snap currently loaded to EPICS db."""
        return self['SDF_LOADED_EDB']

    def sdf_load(self, snap, loadto='both', wait=True):
        """Load SDF snap file to table or EPICS db.
        
        The `loadto` option can be used to specify how the snap file
        is loaded.  The options are:
        
          'both': load into both SDF table and EPICS db (default)
         'table': load into SDF table only
           'edb': load into EPICS db only

        """
        lopts = {
            'both':  1,
            'table': 2,
            'edb':   4,
            }
        assert loadto in lopts.keys(), "Invalid `loadto` value (valid opts: %s)." % lopts.keys()

        s = loadto
        if loadto == 'both':
            s = 'table+edb'
        log("SDF LOAD: %s %s: '%s'" % (self.name.upper(), s, snap))

        self['SDF_NAME'] = snap
        self['SDF_RELOAD'] = lopts[loadto]

        # wait for the readbacks to confirm that the file has been loaded
        if not wait:
            return
        if loadto in ['edb', 'both']:
            while self.sdf_get_loaded_edb() != snap:
                time.sleep(0.01)
        if loadto in ['table', 'both']:
            while self.sdf_get_loaded_table() != snap:
                time.sleep(0.01)

    ##########
    # STATE_WORD

    @property
    def STATE_WORD(self):
        return int(self['STATE_WORD'])

    @property
    def excitation_active(self):
        word = self.STATE_WORD
        return bool(word&(1<<8))

##########

def get_models():
    """Generator of all front-end models

    Include "pseudo" front-end SDF IOCs

    """
    for name, dcuid in sorted(_get_models_autoburt(), key=lambda x: x[1]):
        yield CDSFrontEnd(name, dcuid)


def get_models_dict():
    """Dictionary of front-end models keyed by short name

    """
    return {model.name:model for model in get_models()}

##################################################

summary = "list front end models and DCUIDs"

def main():
    import argparse
    parser = argparse.ArgumentParser(description=summary,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("model", nargs='?',
                        help="model")

    args = parser.parse_args()

    def print_model(model):
        # print(model)
        # return
        print('{} {}'.format(
            model.name,
            model.dcuid
        ))

    if args.model:
        model = CDSFrontEnd.find(args.model)
        print_model(model)

    else:
        for model in get_models():
            print_model(model)


if __name__ == '__main__':
    main()
