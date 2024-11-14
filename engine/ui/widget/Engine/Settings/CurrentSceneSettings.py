from PySide6.QtWidgets import (QWidget, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QFormLayout, QMessageBox, QLayout)

from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
from engine.ui.widget.Engine.Settings.SettingGroup import SettingGroup


class CurrentSceneSettings(SettingGroup):
    def __init__(self, project: Project):
        self.project = project
        self.settings = project.settings

        super().__init__(project, "window.settings.current_scene.button.name")

    def setup_main_layout(self) -> QLayout:
        # Создаем компоненты ввода данных
        self.name_scene = QLineEdit(self.project.get_current_scene().name)

        # Создаем кнопки
        self.apply_button = QPushButton(text_translator.get_translate("window.settings.button.apply"))

        self.apply_button.clicked.connect(self.apply_settings)

        # Размещаем компоненты
        form_layout = QFormLayout()
        form_layout.addRow(text_translator.get_translate("window.settings.current_scene.label.name"), self.name_scene)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        return main_layout

    def apply_settings(self):
        # Сохранение новых значений в Settings
        self.project.get_current_scene().name = self.name_scene.text()