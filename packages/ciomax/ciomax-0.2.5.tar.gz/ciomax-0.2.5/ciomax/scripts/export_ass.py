
from contextlib import contextmanager
import pymxs
import os
from ciomax.renderer import Renderer
from ciomax import camera
import MaxPlus
from ciocore.gpath import Path

rt = pymxs.runtime


@contextmanager
def preserve_state():
    """
    Remember and reset all the properties we change.
    """
    rend_time_type = rt.rendTimeType
    rend_pickup_frames = rt.rendPickupFrames
    rend_nth_frame = rt.rendNThFrame
    rend_export_to_ass = rt.renderers.current.export_to_ass
    rend_ass_file_path = rt.renderers.current.ass_file_path

    yield

    rt.rendTimeType = rend_time_type
    rt.rendPickupFrames = rend_pickup_frames
    rt.rendNThFrame = rend_nth_frame
    rt.renderers.current.export_to_ass = rend_export_to_ass
    rt.renderers.current.ass_file_path = rend_ass_file_path


def main(dialog, *args):

    prefix = args[0]

    ass_files = export_ass_files(dialog, prefix)

    remap_file = write_remap_file(dialog, prefix)

    upload_paths = ass_files + [remap_file]

    environment = [{
        "name": "ARNOLD_PATHMAP",
        "value": Path(remap_file).posix_path(with_drive=False),
        "merge_policy": "exclusive",
    }]

    amendments = {
        "upload_paths": upload_paths,
        "environment": environment
    }

    return amendments


def export_ass_files(dialog, ass_file_prefix):

    renderer = Renderer.get()
    if not renderer.__class__.__name__ == "ArnoldRenderer":
        raise TypeError("If you want to export ass files, please set the current renderer to Arnold.")

    main_sequence = dialog.main_tab.section("FramesSection").main_sequence

    camera_name = dialog.main_tab.section("GeneralSection").camera_component.combobox.currentText()
    print "Set the current view to look through camera: {}",format(camera_name)
    camera.set_view_to(camera_name)
    
    print "Ensure directory is available for ass files"
    _ensure_directory_for(ass_file_prefix)

    print "Closing render setup window if open..."
    if rt.renderSceneDialog.isOpen():
        rt.renderSceneDialog.close()

    with preserve_state():
        print "Setting render time type to use a specified sequence..."
        rt.rendTimeType = 4

        print "Setting the frame range..."
        rt.rendPickupFrames = "{}-{}".format(
            main_sequence.start, main_sequence.end)

        print "Setting the by frame to 1..."
        rt.rendNThFrame = 1

        print "Setting ass export to on..."
        rt.renderers.current.export_to_ass = True

        print "Setting the ass filepath to", "{}.ass".format(ass_file_prefix)
        rt.renderers.current.ass_file_path = "{}.ass".format(ass_file_prefix)

        print "Exporting ass files..."
        rt.render(fromFrame=main_sequence.start,
                  toFrame=main_sequence.end, vfb=False)

        # return list of ass files
        print "Done writing ass files"
        ass_filenames = main_sequence.expand(
            "{}####.ass".format(ass_file_prefix))

    return ass_filenames


def write_remap_file(_, prefix):
    """
    Write a json file that tells Arnold to strip drive letters.
    """
    prefix = prefix.strip(".")
    remap_filename = "{}.json".format(prefix.strip("."))

    lines = []
    lines.append("{\n")
    lines.append('\t"linux": {\n')
    lines.append('\t\t"^[A-Za-z]:": "",\n')
    lines.append('\t\t"^//":"/"\n')
    lines.append('\t}\n')
    lines.append('}\n')

    with open(remap_filename, "w") as fn:
        fn.writelines(lines)

    print "Wrote Arnold remapPathFile file to", remap_filename

    return remap_filename


def _ensure_directory_for(path):
    """
    Ensure that the parent directory of `path` exists
    """
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
