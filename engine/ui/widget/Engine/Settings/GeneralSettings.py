from PySide6.QtWidgets import (QWidget, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QFormLayout, QMessageBox, QLayout)

from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
from engine.ui.widget.Engine.Settings.SettingGroup import SettingGroup


class GeneralSettings(SettingGroup):
    def __init__(self, project: Project):
        self.project = project
        self.settings = project.settings

        super().__init__(project, "window.settings.general.button.name")

    def setup_main_layout(self) -> QLayout:
        # Создаем компоненты ввода данных
        self.name_project_edit = QLineEdit(self.settings.name_project)
        self.version_edit = QLineEdit(self.settings.version)
        self.version_engine_edit = QLineEdit(self.settings.version_engine)
        self.requirements_edit = QLineEdit(self.settings.requirements)
        self.path_assets_edit = QLineEdit(self.settings.path_assets)
        self.path_scene_edit = QLineEdit(self.settings.path_scene)
        self.path_scripts_edit = QLineEdit(self.settings.path_scripts)
        self.compiler_edit = QLineEdit(self.settings.compiler)
        self.fps_edit = QSpinBox()
        self.fps_edit.setRange(1, 240)
        self.fps_edit.setValue(self.settings.fps)
        self.width_window_edit = QSpinBox()
        self.width_window_edit.setRange(100, 3840)
        self.width_window_edit.setValue(self.settings.width_window)
        self.height_window_edit = QSpinBox()
        self.height_window_edit.setRange(100, 2160)
        self.height_window_edit.setValue(self.settings.height_window)

        # Создаем кнопки
        self.apply_button = QPushButton(text_translator.get_translate("window.settings.button.apply"))

        self.apply_button.clicked.connect(self.apply_settings)

        # Размещаем компоненты
        form_layout = QFormLayout()
        form_layout.addRow("Имя проекта:", self.name_project_edit)
        form_layout.addRow("Версия:", self.version_edit)
        form_layout.addRow("Версия движка:", self.version_engine_edit)
        form_layout.addRow("Требования:", self.requirements_edit)
        form_layout.addRow("Путь к ассетам:", self.path_assets_edit)
        form_layout.addRow("Путь к сценам:", self.path_scene_edit)
        form_layout.addRow("Путь к скриптам:", self.path_scripts_edit)
        form_layout.addRow("Компилятор:", self.compiler_edit)
        form_layout.addRow("FPS:", self.fps_edit)
        form_layout.addRow("Ширина окна:", self.width_window_edit)
        form_layout.addRow("Высота окна:", self.height_window_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        return main_layout

    def apply_settings(self):
        # Сохранение новых значений в Settings
        self.settings.set_name_project(self.name_project_edit.text())
        self.settings.set_version(self.version_edit.text())
        self.settings.set_version_engine(self.version_engine_edit.text())
        self.settings.set_requirements(self.requirements_edit.text())
        self.settings.set_path_assets(self.path_assets_edit.text())
        self.settings.set_path_scene(self.path_scene_edit.text())
        self.settings.set_path_scripts(self.path_scripts_edit.text())
        self.settings.set_compiler(self.compiler_edit.text())
        self.settings.set_fps(self.fps_edit.value())
        self.settings.set_width_window(self.width_window_edit.value())
        self.settings.set_height_window(self.height_window_edit.value())