from PySide2 import QtWidgets, QtGui, QtCore
import MaxPlus
from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp
from ciomax.components.combo_box_grp import ComboBoxGrp, InstanceTypeComboBoxGrp
from ciocore import data as coredata
from ciomax import camera

class GeneralSection(CollapsibleSection):
    ORDER = 10



    def __init__(self, dialog):
        super(GeneralSection, self).__init__(dialog, "General")

        self.title_component = TextFieldGrp(
            label="Job Title", 
            tooltip="The title that appears in the Conductor web dashboard on the jobs page.")

        self.project_component = ComboBoxGrp(label="Conductor Project")
        self.instance_type_component = InstanceTypeComboBoxGrp()

        self.destination_component = TextFieldGrp(
            label="Destination",
            directory=True,
            placeholder="Path where renders are saved to"
        )

        self.camera_component = ComboBoxGrp(label="Camera")

        self.content_layout.addWidget(self.title_component)
        self.content_layout.addWidget(self.project_component)
        self.content_layout.addWidget(self.instance_type_component)
        self.content_layout.addWidget(self.destination_component)
        self.content_layout.addWidget(self.camera_component)

        self.set_project_model()
        self.set_camera_model()
        self.set_instance_type_model()
        self.configure_signals()

    def set_project_model(self):
        if not coredata.valid():
            print "Invalid projects data"
            return False

        model = QtGui.QStandardItemModel()
        for project in coredata.data()["projects"] or []:
            model.appendRow(QtGui.QStandardItem(project))
        self.project_component.set_model(model)
        return True

    def set_camera_model(self):
        cam_names = camera.collect_cameras()
        model = QtGui.QStandardItemModel()
        for cam_name in cam_names or []:
            model.appendRow(QtGui.QStandardItem(cam_name))
        self.camera_component.set_model(model)
        return True

    def set_instance_type_model(self):
        if not coredata.valid():
            print "Invalid Instance Types"
            return False

        model = QtGui.QStandardItemModel()
        cpu_item = QtGui.QStandardItem("CPU")
        gpu_item = QtGui.QStandardItem("GPU")
        for entry in coredata.data()["instance_types"] or []:
            if entry.get("gpu"):
                gpu_item.appendRow((QtGui.QStandardItem(
                    entry["description"]), QtGui.QStandardItem(entry["name"])))
            else:
                cpu_item.appendRow((QtGui.QStandardItem(
                    entry["description"]), QtGui.QStandardItem(entry["name"])))
        model.appendRow(cpu_item)
        model.appendRow(gpu_item)

        self.instance_type_component.set_model(model)

        return True

    def configure_signals(self):
        """Write to store when values change"""
        self.title_component.field.editingFinished.connect(
            self.on_title_change)

        self.project_component.combobox.currentTextChanged.connect(
            self.on_project_change)

        self.camera_component.combobox.currentTextChanged.connect(
            self.on_camera_change)

        self.instance_type_component.combobox_machine.currentTextChanged.connect(
            self.on_instance_type_change)

        self.instance_type_component.checkbox.stateChanged.connect(
            self.on_preemptible_change)

        self.destination_component.field.editingFinished.connect(
            self.on_destination_change)

        self.destination_component.button.clicked.connect(
            self.on_destination_change)

    def on_title_change(self):
        self.dialog.store.set_title(self.title_component.field.text())

    def on_project_change(self, value):
        self.dialog.store.set_project(value)

    def on_camera_change(self, value):
        self.dialog.store.set_camera(value)

    def on_instance_type_change(self, value):
        short_name = self.instance_type_component.get_item_name(value)
        self.dialog.store.set_instance_type(short_name)

    def on_preemptible_change(self, value):
        self.dialog.store.set_preemptible(value > 0)

    def on_destination_change(self):
        self.dialog.store.set_destination(
            self.destination_component.field.text())

    def populate_from_store(self):
        store = self.dialog.store

        super(GeneralSection, self).populate_from_store(store )

        self.title_component.field.setText(store.title())

        self.destination_component.field.setText(store.destination())
        self.project_component.set_by_text(store.project())
        self.camera_component.set_by_text(store.camera())
        
        self.instance_type_component.set_by_text(
            store.instance_type(), column=1)

        self.instance_type_component.checkbox.setCheckState(
            QtCore.Qt.Checked if store.preemptible() else QtCore.Qt.Unchecked)

    def resolve(self, expander, **kwargs):

        return {
            "job_title": expander.evaluate(self.title_component.field.text()),
            "output_path":  expander.evaluate(self.destination_component.field.text()),
            "project": self.project_component.combobox.currentText(),
            "instance_type":  self.instance_type_component.get_current_item_name(),
            "preemptible": self.instance_type_component.checkbox.isChecked()
        }
