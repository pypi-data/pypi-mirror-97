import sys
import os

from PySide2 import QtWidgets 
from pymxs import runtime as rt
import MaxPlus
import datetime
# DO NOT SORT IMPORTS !!!!!!!!!!!!!
CONDUCTOR_LOCATION = os.path.dirname(os.path.dirname(__file__))
sys.path.append(CONDUCTOR_LOCATION)

# While in development, we reload classes when this file is executed.
from ciomax import reloader
reload(reloader)

from ciomax.preview_tab import PreviewTab
from ciomax.main_tab import MainTab
from ciomax.validation_tab import ValidationTab
from ciomax.response_tab import ResponseTab

from ciomax.store import ConductorStore
from ciocore.gpath import Path
from ciocore import data as coredata
FIXTURES_DIR = os.path.expanduser(os.path.join("~", "Conductor", "fixtures"))


BACKGROUND_COLOR = "rgb(48, 48, 48)"
STYLESHEET = """
QLineEdit {{ background: {bg}; }}
QSpinBox {{ background: {bg}; }}
QListWidget {{ background: {bg}; }}
QToolButton {{ border: none; }}
QTextEdit {{ background: {bg}; }}""".format(bg=BACKGROUND_COLOR)


class ConductorDialog(QtWidgets.QDialog):
    """
    Build the dialog as a child of the Max window.

    We build a tab layout, and the first tab contains the main controls.
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(
            self, QtWidgets.QWidget.find(rt.windows.getMAXHWND()))

        self.store = ConductorStore()
        coredata.init(product="all")
        coredata.set_fixtures_dir(
            FIXTURES_DIR if self.store.use_fixtures() else "")
        coredata.data(force=True)

        self.screen_scale = self.logicalDpiX() / 96

        self.setStyleSheet(STYLESHEET)
        self.setWindowTitle("Conductor")
        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()

        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)

        self.main_tab = MainTab(self)
        self.preview_tab = PreviewTab(self)
        self.validation_tab = ValidationTab(self)
        self.response_tab = ResponseTab(self)

        self.tab_widget.addTab(self.main_tab, "Configure")
        self.tab_widget.addTab(self.preview_tab, "Preview")
        self.tab_widget.addTab(self.validation_tab, "Validation")
        self.tab_widget.addTab(self.response_tab, "Response")

        self.tab_widget.setTabEnabled(2, False)
        self.tab_widget.setTabEnabled(3, False)

        self.main_tab.populate_from_store()
        self.configure_signals()

    def show_main_tab(self):
        self.tab_widget.setCurrentWidget(self.main_tab)

    def show_preview_tab(self):
        self.tab_widget.setCurrentWidget(self.preview_tab)

    def show_validation_tab(self):
        self.tab_widget.setTabEnabled(2, True)
        self.validation_tab.clear()
        self.tab_widget.setCurrentWidget(self.validation_tab)

    def show_response_tab(self):
        self.tab_widget.setTabEnabled(3, True)
        self.response_tab.clear()
        self.tab_widget.setCurrentWidget(self.response_tab)

    def configure_signals(self):
        self.tab_widget.currentChanged.connect(self.on_tab_change)

    def on_tab_change(self, index):
        if index == 1:
            context = self.get_context()
            submission = self.main_tab.resolve(context)
            self.preview_tab.populate(submission)
        if index != 2:
            self.tab_widget.setTabEnabled(2, False)

    def get_context(self):
        scenefile = MaxPlus.FileManager.GetFileNameAndPath()
        if scenefile:
            scenefile = Path(scenefile).posix_path()
            scenedir = os.path.dirname(scenefile)
            scenenamex, ext = os.path.splitext(os.path.basename(scenefile))
        else:
            scenefile = "/NOT_SAVED"
            scenedir = "/NOT_SAVED"
            scenenamex, ext = ("NOT_SAVED", "")
        scenename = "{}{}".format(scenenamex, ext)

        project = MaxPlus.Core.EvalMAXScript(
            'pathConfig.getCurrentProjectFolder()').Get()
        if project:
            project = Path(project).posix_path()
        else:
            project = "/NOT_SET"

        result = {
            "conductor": Path(CONDUCTOR_LOCATION).posix_path(),
            "scenefile": scenefile,
            "scenedir": scenedir,
            "scenenamex": scenenamex,
            "ext": ext,
            "scenename": scenename,
            "project": project,
            "renderer": MaxPlus.RenderSettings.GetProduction().GetClassName(),
            "timestamp": datetime.datetime.now().strftime('%y%m%d_%H%M%S')
        }
        return result


def main():

    dlg = ConductorDialog()
    dlg.resize(600 * dlg.screen_scale, 800 * dlg.screen_scale)

    # exec_() causes the window to be modal. This means we don't have to manage
    # any communication between max and the dialog, like changes to the frame
    # range while the dialog is open.
    dlg.exec_()


if __name__ == '__main__':
    main()
