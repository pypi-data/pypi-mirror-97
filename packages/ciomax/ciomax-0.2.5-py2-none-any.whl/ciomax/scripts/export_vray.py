
import pymxs
import os
from ciomax.renderer import Renderer
from ciomax import camera
from ciocore.gpath_list import PathList
from ciocore.gpath import Path

import MaxPlus

from contextlib import contextmanager


@contextmanager
def maintain_save_state():
    required = rt.getSaveRequired()
    yield
    rt.setSaveRequired(required)


rt = pymxs.runtime


@contextmanager
def preserve_state():
    """
    Remember and reset all the properties we change.
    """
    rend_time_type = rt.rendTimeType
    rend_pickup_frames = rt.rendPickupFrames
    rend_nth_frame = rt.rendNThFrame

    yield

    rt.rendTimeType = rend_time_type
    rt.rendPickupFrames = rend_pickup_frames
    rt.rendNThFrame = rend_nth_frame



def main(dialog, *args):
    """
    Export assets needed for a vray render.

    We need the vrscene file, and we need file that defines mappings between the
    Windows paths and linux paths on the render nodes. This mapping is always
    simply removing a drive letter or in the case of UNC paths, removing the
    extra leading slash.
    """
    prefix = os.path.splitext(args[0])[0]

    vray_scene = export_vrscene(dialog, prefix)

    remap_file = write_remap_file(prefix, vray_scene)

    # Return both the vray scene and the remapFile so they are both uploaded.

    amendments = {
        "upload_paths": [vray_scene, remap_file]
    }
    return amendments


def export_vrscene(dialog, vrscene_prefix):


    renderer = Renderer.get()
    valid_renderers = ["VrayGPURenderer", "VraySWRenderer"]

    if not renderer.__class__.__name__ in valid_renderers:
        raise TypeError(
            "Please the current renderer to one of: {}".format(valid_renderers))

    main_sequence = dialog.main_tab.section("FramesSection").main_sequence

    camera_name = dialog.main_tab.section("GeneralSection").camera_component.combobox.currentText()
    print "Set the current view to look through camera: {}",format(camera_name)
    camera.set_view_to(camera_name)

    print "Ensure directory is available for vrscene_file"
    _ensure_directory_for(vrscene_prefix)

    print "Closing render setup window if open..."
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()

    with preserve_state():
        print "Setting render time type to use a specified sequence..."
        rt.rendTimeType = 4

        print "Setting the frame range..."
        rt.rendPickupFrames = "{}-{}".format(main_sequence.start,
                                            main_sequence.end)

        print "Setting the by frame to 1..."
        rt.rendNThFrame = 1

        print "Exporting vrscene files"
        error = 0
        with maintain_save_state():
            error = rt.vrayExportRTScene(
                vrscene_prefix,
                startFrame=main_sequence.start,
                endFrame=main_sequence.end)

        vray_scene = "{}.vrscene".format(vrscene_prefix)
        if os.path.exists(vray_scene):
            if error:
                print "Scene was exported, but there were errors during export. Check %temp%/vraylog.txt"
            else:
                print "Scene was exported successfully"
        else:
            raise ValueError("Vray scene export failed. Check %temp%/vraylog.txt")

        # return list of extra dependencies
        print "Completed vrscene export.."

    return vray_scene


def write_remap_file(prefix, vray_scene):
    assets = [asset.GetResolvedFileName()
              for asset in list(MaxPlus.AssetManager.GetAssets())]
    assets += [vray_scene]
    pathlist = PathList(*assets)

    prefix_set = set()

    for p in pathlist:
        prefix_set.add(Path(p.all_components[:2]).posix_path())

    remap_filename = "{}.xml".format(prefix)

    lines = []
    lines.append("<RemapPaths>\n")
    for p in prefix_set:
        pth = Path(p)
        lines.append("\t<RemapItem>\n")
        lines.append("\t\t<From>{}</From>\n".format(pth.posix_path()))
        lines.append(
            "\t\t<To>{}</To>\n".format(pth.posix_path(with_drive=False)))
        lines.append("\t</RemapItem>\n")
    lines.append("</RemapPaths>\n")
    with open(remap_filename, "w") as fn:
        fn.writelines(lines)

    print "Wrote Vray remapPathFile file to", remap_filename

    return remap_filename


def _ensure_directory_for(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
