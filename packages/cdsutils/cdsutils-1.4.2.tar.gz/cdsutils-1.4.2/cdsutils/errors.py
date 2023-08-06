class CdsutilsError(Exception):
    pass

class CliError(SystemExit):
    def __init__(self, msg):
        super(CliError, self).__init__("ERROR: %s" % msg)
