 
 
import MaxPlus 
from pymxs import runtime as rt
from ciomax.const import MAYA_BASE_VERSION

class Renderer(object):
    """A collection of frames with the ability to generate chunks."""

    # Prevents user from using constructor. Use Factory (get()) instead.
    __magic_shield = object()
 

    @classmethod
    def get(cls):
        """Factory which will create a Renderer."""

        name = str(rt.renderers.current).split(":")[0]
        if name.startswith("V_Ray_GPU"):
            return VrayGPURenderer(cls.__magic_shield, name)
        elif name.startswith("V_Ray"):
            return VraySWRenderer(cls.__magic_shield, name)
        elif name == "Arnold":
            return ArnoldRenderer(cls.__magic_shield, name)
        else:
            return InvalidRenderer(cls.__magic_shield, name)

    def __init__(self, _shield, name):
        assert (
            _shield == Renderer.__magic_shield
        ), "Renderer must be created with Renderer.get()"

        self._name = name
        self.version = self.get_version()


    def __str__(self):
        return str(self._name)
 
    @staticmethod
    def get_version():
        return "none 0.0.0.0"


class VraySWRenderer(Renderer):
    def __init__(self, _shield, name):
        super(VraySWRenderer, self).__init__(_shield, name)

        self.templates = [
            {
                "name": "default" , 
                "command": 'vray  -display=0 -verboseLevel=4 -sceneFile="<posix project>/vray/<timestamp>_<scenenamex>.vrscene"  -remapPathFile="<posix project>/vray/<timestamp>_<scenenamex>.xml"   -imgFile="<posix project>/renderoutput/<scenenamex>.exr" -frames=<start>-<end>',
                "script":u'"<conductor>/ciomax/scripts/export_vray.py" "<project>/vray/<timestamp>_<scenenamex>"'
            }
        ]

    @staticmethod
    def get_version():
        parts = rt.vrayVersion()[0].split('.')
        version = ".".join(parts + ["0"] * (4 - len(parts)))
        return "v-ray-standalone {}".format(version)


class VrayGPURenderer(VraySWRenderer):
    def __init__(self, _shield, name):
        super(VrayGPURenderer, self).__init__(_shield, name)


class ArnoldRenderer(Renderer):
    def __init__(self, _shield, name):
        super(ArnoldRenderer, self).__init__(_shield, name)
        self.templates = [
            {
                "name": "default" , 
                "command": u'kick -nostdin -i "<posix project>/ass/<timestamp>/<scenenamex>.<pad start 4>.ass" -dw -dp -v 5 -of exr -o "<posix project>/renderoutput/<scenenamex>.<pad start 4>.exr"',
                "script": u'"<conductor>/ciomax/scripts/export_ass.py" "<project>/ass/<timestamp>/<scenenamex>."'
           }
        ]
    
    @staticmethod
    def get_version():
        for i in range(MaxPlus.PluginManager.GetNumPluginDlls()):
            dll = MaxPlus.PluginManager.GetPluginDll(i)
            if dll.GetDescription() == 'Arnold':
                path = dll.GetFilePath()
                parts = rt.getFileVersion(path).split("\t")[0].split(",")
                version = ".".join(parts + ["0"] * (4 - len(parts)))
                return "{}/arnold-maya {}".format(MAYA_BASE_VERSION, version)

class InvalidRenderer(Renderer):
    def __init__(self, _shield, name):
        super(InvalidRenderer, self).__init__(_shield, name)
        
        self.templates = [
            {
                "name": "default" , 
                "command": '',
                "script": ''
            }
        ]
    @staticmethod
    def get_version():
        return "none 0.0.0.0"
