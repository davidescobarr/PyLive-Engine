from PySide6.QtWidgets import (QWidget, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QFormLayout, QMessageBox, QLayout)

from core.compiler.Compiler import compile_with_pyinstaller
from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator, TextTranslater
from engine.ui.widget.Engine.Settings.SettingGroup import SettingGroup


class CompileSettings(SettingGroup):
    def __init__(self, project: Project):
        self.project = project
        self.settings = project.settings

        super().__init__(project, "window.settings.compile.button.name")

    def setup_main_layout(self) -> QLayout:
        # Размещаем компоненты
        form_layout = QFormLayout()
        form_layout.addRow(text_translator.get_translate("window.settings.compile.name_project.name"), QLabel(self.settings.name_project))
        form_layout.addRow(text_translator.get_translate("window.settings.compile.version.name"), QLabel(self.settings.version))
        form_layout.addRow(text_translator.get_translate("window.settings.compile.compiler.name"), QLabel(self.settings.compiler))

        self.status_label = QLabel(text_translator.get_translate("window.settings.compile.compilation_not_started.name"))

        # Создаем кнопки
        self.compile_button = QPushButton(text_translator.get_translate("window.settings.button.compile"))

        self.compile_button.clicked.connect(self.compile)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.compile_button)
        button_layout.addWidget(self.status_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        return main_layout

    def compile(self):
        self.status_label.setText(text_translator.get_translate("window.settings.compile.compilation_started.name"))
        output = compile_with_pyinstaller(self.settings)
        if output == "0":
            self.status_label.setText(text_translator.get_translate("window.settings.compile.compilation_successfully.name"))
        else:
            self.status_label.setText(output)