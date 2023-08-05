import MaxPlus


def collect_cameras():
    root = MaxPlus.Core.GetRootNode()
    result = []
    _collect_all_cameras(root, result)
    return result


def set_view_to(name):
    camera = _find_camera(name)
    current_viewport = MaxPlus.ViewportManager.GetActiveViewport()
    current_viewport.SetViewCamera(camera)


def _is_cam(node):
    obj = node.Object
    return obj and obj.GetSuperClassID() == MaxPlus.SuperClassIds.Camera


def _collect_all_cameras(node, names):
    if _is_cam(node):
        names.append(node.Name)
    for child in node.Children:
        _collect_all_cameras(child, names)


def _find_camera(name, node=None):
    if not node:
        node = MaxPlus.Core.GetRootNode()

    if _is_cam(node) and node.Name == name:
        return node
    for child in node.Children:
        result = _find_camera(name, child)
        if result:
            return result
