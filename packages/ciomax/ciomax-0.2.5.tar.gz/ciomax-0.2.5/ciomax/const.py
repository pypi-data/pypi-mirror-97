import os
VERSION = u"dev.999"
PLUGIN_DIR = os.path.dirname(__file__)
try:
    with open(os.path.join(PLUGIN_DIR, "VERSION")) as version_file:
        VERSION = version_file.read().strip()
except BaseException:
    pass

MAYA_BASE_VERSION = "maya-io 2019.SP3"