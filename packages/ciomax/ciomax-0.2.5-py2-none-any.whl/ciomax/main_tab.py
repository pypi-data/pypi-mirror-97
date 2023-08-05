
import os
from PySide2 import QtWidgets, QtCore, QtGui
from ciocore.expander import Expander
from ciomax.sections.collapsible_section import CollapsibleSection

from ciomax.sections.general_section import GeneralSection
from ciomax.sections.software_section import SoftwareSection
from ciomax.sections.frames_section import FramesSection
from ciomax.sections.info_section import InfoSection
from ciomax.sections.environment_section import EnvironmentSection
from ciomax.sections.metadata_section import MetadataSection
from ciomax.sections.extra_assets_section import ExtraAssetsSection
from ciomax.sections.advanced_section import AdvancedSection
from ciomax import submit, renderer

from ciomax.components.buttoned_scroll_panel import ButtonedScrollPanel

from ciocore.gpath import Path


class MainTab(ButtonedScrollPanel):
    """
    Build the tab that contains the main configuration sections.
    """

    def __init__(self, dialog):
        super(MainTab, self).__init__(
            dialog,
            buttons=[("close", "Close"),  ("submit", "Validate and Submit")])

        self._section_classes = sorted(
            CollapsibleSection.__subclasses__(), key=lambda x: x.ORDER)
        self.sections = [cls(self.dialog) for cls in self._section_classes]

        for section in self.sections:
            self.layout.addWidget(section)

        self.layout.addStretch()
        self.configure_signals()

    def populate_from_store(self):
        for section in self.sections:
            section.populate_from_store()

    def configure_signals(self):
        self.buttons["close"].clicked.connect(self.dialog.close)

        self.buttons["submit"].clicked.connect(self.on_submit_button)

    def on_submit_button(self):
        submit.submit(self.dialog)

    def section(self, classname):
        """
        Convenience to find sections by name.

        Makes it easier to allow sections to talk to each other.
        Example: Calculate info from stuff in the frames section
            self.section("InfoSection").calculate(self.section("FramesSection"))

        """

        return next(s for s in self.sections if s.__class__.__name__ == classname)

    def resolve(self, context, **kwargs):
        """
        Resolve the submission object based on the values in the UI.

        kwargs may contain an amendments object, which is whatever a
        pre-submission script decided to return. This is usually a list of extra
        files to upload, but can contain any valid submission key, such as extra
        environment entries. In any case, it is passed along to each section's
        resolve method so it may handle merging the appropriate fields.
        """
        submission = {}
        expander = Expander(safe=True, **context)
        for section in self.sections:
            submission.update(section.resolve(expander, **kwargs))
        return submission
