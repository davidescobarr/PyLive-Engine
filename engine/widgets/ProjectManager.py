import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal


class ProjectManager(QWidget):
    open_project_signal = pyqtSignal(str)  # Сигнал для открытия проекта

    def __init__(self):
        super().__init__()

    def load(self) -> bool:
        if not self.load_last_project():
            self.init_ui()
            return False
        return True

    def init_ui(self):
        layout = QVBoxLayout()

        # Кнопка для открытия проекта
        open_button = QPushButton("Open Project")
        open_button.setFixedWidth(150)
        open_button.setFixedHeight(30)
        open_button.setStyleSheet("background-color: #4F44E5; border-radius: 15px; width: 150px; height: 30px; cursor: pointer; color: #fff;")
        open_button.clicked.connect(self.open_project)
        layout.addWidget(open_button)

        # Кнопка для создания нового проекта
        new_button = QPushButton("Create New Project")
        new_button.setFixedWidth(150)
        new_button.setFixedHeight(30)
        new_button.setStyleSheet("background-color: #4F44E5; border-radius: 15px; cursor: pointer; color: #fff;")
        new_button.clicked.connect(self.create_new_project)
        layout.addWidget(new_button)

        self.setLayout(layout)

    def open_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if not project_dir:
            return

        if not self.validate_project_directory(project_dir):
            return

        # Сохранение пути к последнему проекту
        self.save_last_project(project_dir)

        self.open_project_signal.emit(project_dir)

    def create_new_project(self):
        project_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Create Project")
        if not project_dir:
            return

        # Базовые настройки для нового проекта
        settings = {
            "current_project": "New Game Project",
            "version": "1.0"
        }

        settings_path = os.path.join(project_dir, 'settings.json')

        # Запись файла settings.json
        with open(settings_path, 'w') as file:
            json.dump(settings, file, indent=4)

        # Создание необходимых директорий
        os.makedirs(os.path.join(project_dir, 'assets'), exist_ok=True)
        os.makedirs(os.path.join(project_dir, 'scripts'), exist_ok=True)
        os.makedirs(os.path.join(project_dir, 'scene'), exist_ok=True)

        QMessageBox.information(self, "Project Created", "New project created successfully!")

        # Сохранение пути к новому проекту
        self.save_last_project(project_dir)

        self.open_project_signal.emit(project_dir)

    def validate_project_directory(self, project_dir):
        """Проверка на наличие settings.json."""
        settings_path = os.path.join(project_dir, 'settings.json')
        if not os.path.exists(settings_path):
            QMessageBox.warning(self, "Error", "settings.json not found in the selected directory.")
            return False
        return True

    def save_last_project(self, project_dir):
        with open("settings.json", 'w') as file:
            json.dump({"last_project_path": project_dir}, file)

    def load_last_project(self) -> bool:
        if os.path.exists("settings.json"):
            with open("settings.json", 'r') as file:
                data = json.load(file)
                project_dir = data.get("last_project_path")
                if project_dir and self.validate_project_directory(project_dir):
                    self.open_project_signal.emit(project_dir)
                    return True
        return False