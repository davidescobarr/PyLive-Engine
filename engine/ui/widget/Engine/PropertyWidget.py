from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QCheckBox, QMessageBox, QTreeWidget
)
from core.scene.components.Object import SceneObject
from core.utils.FinderDecorators import find_visible_properties
from core.utils.delegates.PropertyValueDelegate import property_value_delegate


class PropertyEditor(QWidget):
    def __init__(self, obj: SceneObject = None, parent=None):
        super().__init__(parent)
        self.obj = obj
        self.form_layout = QFormLayout()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.setLayout(self.main_layout)
        if obj:
            self.set_current_object(obj)
        self.setWindowTitle("Property Editor")
        property_value_delegate.subscribe(self.update_value_property)
        self.setAutoFillBackground(True)

    def set_current_object(self, obj: SceneObject):
        """Set the current object and update the form layout."""
        self.obj = obj
        self.clear_form_layout()
        self.create_form_fields()

    def update_value_property(self, func):
        """Update the property value in the widget if the property changes."""
        property_name = self._find_property_name(func)
        if property_name:
            self._update_widget_value(property_name)

    def create_form_fields(self):
        """Create form fields for the properties of the object."""
        if isinstance(self.obj, SceneObject):
            for path, name, value in find_visible_properties(self.obj.object):
                if isinstance(value, bool):
                    self._add_checkbox(name, value)
                else:
                    self._add_line_edit(name, value)

    def update_property(self):
        """Update the object property based on the widget value."""
        sender = self.sender()
        attribute = sender.objectName()
        value = self._get_widget_value(sender, attribute)
        # Try to cast the value to the correct type
        casted_value = self._cast_value(value, getattr(self.obj.object, attribute))
        if casted_value is None:
            QMessageBox.warning(self, "Ошибка", "Неверно указана переменная")
            # Reset the value in the widget to the original property value if casting failed
            self._update_widget_value(attribute)
            return
        setattr(self.obj.object, attribute, casted_value)

    def clear_form_layout(self):
        """Remove all widgets from the form layout."""
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _find_property_name(self, func):
        if not self.obj or not isinstance(self.obj, SceneObject):
            return None
        """Find the property name by its accessor function."""
        for name, attr in self.obj.object.__class__.__dict__.items():
            if attr is func:
                return name
        return None

    def _update_widget_value(self, property_name):
        """Update the widget value for a given property."""
        widget_line = self.findChild(QLineEdit, property_name)
        widget_check = self.findChild(QCheckBox, property_name)
        if widget_line:
            value = getattr(self.obj.object, property_name)
            widget_line.setText(str(value))
        elif widget_check:
            value = getattr(self.obj.object, property_name)
            widget_check.setChecked(value)

    def _add_checkbox(self, name, value):
        """Add a checkbox to the form layout."""
        checkbox = QCheckBox()
        checkbox.setChecked(value)
        checkbox.setObjectName(name)
        checkbox.stateChanged.connect(self.update_property)
        self.form_layout.addRow(QLabel(name), checkbox)

    def _add_line_edit(self, name, value):
        """Add a line edit to the form layout."""
        line_edit = QLineEdit(str(value))
        line_edit.setObjectName(name)
        line_edit.editingFinished.connect(self.update_property)
        self.form_layout.addRow(QLabel(name), line_edit)

    def _get_widget_value(self, sender, attribute):
        """Get the value from the widget."""
        if isinstance(sender, QLineEdit):
            return sender.text()
        elif isinstance(sender, QCheckBox):
            return sender.isChecked()
        return None

    def _cast_value(self, value, current_value):
        """Cast the value to the appropriate type based on the current value."""
        try:
            if isinstance(current_value, int):
                return int(value)
            elif isinstance(current_value, float):
                return float(value)
            elif isinstance(current_value, bool):
                return value.lower() in ["true", "1", "yes"]
            return value
        except ValueError:
            return None
