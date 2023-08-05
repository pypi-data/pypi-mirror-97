from PySide2 import QtCore, QtWidgets
import re
import shlex
from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp
from ciomax.components.checkbox_grp import CheckboxGrp

from ciomax.components.int_field_grp import IntFieldGrp
from ciocore.expander import Expander
from ciocore.gpath import Path
import imp


class AdvancedSection(CollapsibleSection):
    ORDER = 100

    def __init__(self, dialog):
        super(AdvancedSection, self).__init__(dialog, "Advanced")

        self.script_component = TextFieldGrp(
            label="Pre submission script",
            enablable=True,
            custom_button="Execute",
            placeholder="Python script"
        )
        self.content_layout.addWidget(self.script_component)

        self.task_template_component = TextFieldGrp(
            label="Task template",
            enablable=False)
        self.content_layout.addWidget(self.task_template_component)

        self.add_separator()

        self.retry_preempted_component = IntFieldGrp(
            label="Preempted retries", default=1, minimum=0, maximum=5)
        self.content_layout.addWidget(self.retry_preempted_component)

        self.notification_component = TextFieldGrp(
            label="Send Notifications",
            enablable=True)
        self.content_layout.addWidget(self.notification_component)

        self.location_component = TextFieldGrp(
            label="Location tag")
        self.content_layout.addWidget(self.location_component)

        upload_options_component = CheckboxGrp(
            label="Uploads",
            checkboxes=1,
            sublabels=["Use upload daemon"]
        )
        self.use_daemon_checkbox = upload_options_component.checkboxes[0]

        self.content_layout.addWidget(upload_options_component)

        self.add_separator()

        diagnostics_options_grp = CheckboxGrp(
            label="Developer",
            checkboxes=2,
            sublabels=["Show tracebacks", "Use fixtures"]
        )

        self.tracebacks_checkbox = diagnostics_options_grp.checkboxes[0]
        self.fixtures_checkbox = diagnostics_options_grp.checkboxes[1]
        self.content_layout.addWidget(diagnostics_options_grp)

        self.configure_signals()

    def configure_signals(self):
        """Write to store when values change."""

        self.task_template_component.field.editingFinished.connect(
            self.on_task_template_change)

        self.retry_preempted_component.field.valueChanged.connect(
            self.on_retry_preempted_change)

        self.notification_component.field.editingFinished.connect(
            self.on_notification_change)

        self.notification_component.display_checkbox.stateChanged.connect(
            self.on_use_notification_change)

        self.location_component.field.editingFinished.connect(
            self.on_location_change)

        # DAEMON
        self.use_daemon_checkbox.clicked.connect(
            self.on_use_daemon_change)

        self.tracebacks_checkbox.clicked.connect(
            self.on_show_tracebacks_change)

        self.fixtures_checkbox.clicked.connect(
            self.on_use_fixtures_change)

        self.script_component.display_checkbox.stateChanged.connect(
            self.on_use_script_change)

        self.script_component.field.editingFinished.connect(
            self.on_script_change)

        self.script_component.button.clicked.connect(
            self.on_script_button)

    def on_task_template_change(self):
        self.dialog.store.set_task_template(
            self.task_template_component.field.text())

    def on_retry_preempted_change(self, value):
        self.dialog.store.set_retries_when_preempted(value)

    def on_notification_change(self):
        self.dialog.store.set_emails(self.notification_component.field.text())

    def on_use_notification_change(self, value):
        self.dialog.store.set_use_emails(value > 0)

    def on_location_change(self):
        self.dialog.store.set_location_tag(
            self.location_component.field.text())

    def on_use_daemon_change(self, value):
        self.dialog.store.set_use_upload_daemon(value > 0)

    def on_show_tracebacks_change(self, value):
        self.dialog.store.set_show_tracebacks(value > 0)

    def on_use_fixtures_change(self, value):
        self.dialog.store.set_use_fixtures(value > 0)

    def on_use_script_change(self, value):
        self.dialog.store.set_use_script(value > 0)

    def on_script_change(self):
        self.dialog.store.set_script_filename(
            self.script_component.field.text())

    def on_script_button(self):
        """Run the presubmission script.

        Once we have the amendments, resolve the whole submission, with
        amendments merged in, and show it in the Preview panel.
        """
        context = self.dialog.get_context()
        amendments = self.run_presubmit_script(context)

        submission = self.dialog.main_tab.resolve(
            context, amendments=amendments)

        self.dialog.show_preview_tab()
        self.dialog.preview_tab.populate(submission)

    def run_presubmit_script(self, context):

        main_sequence = self.dialog.main_tab.section(
            "FramesSection").main_sequence
        context.update({
            "start": main_sequence.start,
            "end": main_sequence.end
        })
        expander = Expander(safe=True, **context)

        cmd = expander.evaluate(self.script_component.field.text())

        parts = shlex.split(cmd)
        if not parts:
            raise ValueError("Enter full path to script followed by args")

        script_path = Path(parts[0]).posix_path()

        args = [self.dialog] + parts[1:]
        # There used to be a try/catch here, but it suppressed the traceback.
        # Better to just show the trace.
        script_module = imp.load_source("", script_path)
        return script_module.main(*args)

    def populate_from_store(self):
        store = self.dialog.store
        super(AdvancedSection, self).populate_from_store(store)

        self.task_template_component.field.setText(store.task_template())

        self.script_component.set_active(store.use_script())
        self.script_component.field.setText(store.script_filename())

        self.retry_preempted_component.field.setValue(
            store.retries_when_preempted())

        self.notification_component.field.setText(store.emails())
        self.notification_component.set_active(store.use_emails())

        self.location_component.field.setText(store.location_tag())

        use_daemon = store.use_upload_daemon()
        self.use_daemon_checkbox.setChecked(use_daemon)

        self.tracebacks_checkbox.setChecked(store.show_tracebacks())
        self.fixtures_checkbox.setChecked(store.use_fixtures())

        return

    def resolve(self, expander, **kwargs):
        location = expander.evaluate(self.location_component.field.text())

        result = {}

        result["autoretry_policy"] = {
            "preempted": {
                "max_retries": self.retry_preempted_component.field.value()
            }
        }

        if self.notification_component.display_checkbox.isChecked():
            emails = list(filter(None, re.split(
                r"[, ]+",  self.notification_component.field.text())))
            if emails:
                result["notify"] = emails

        if location:
            result["location"] = location

        result["local_upload"] = not self.use_daemon_checkbox.isChecked()

        return result
