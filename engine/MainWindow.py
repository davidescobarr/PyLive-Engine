import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow, QWidget,
    QGridLayout, QMenu, QMessageBox, QMenuBar
)
from PyQt6.QtGui import QAction

from engine.Project import Project
from engine.widgets.FileBrowser import FileBrowser
from engine.widgets.HierarchyWidget import HierarchyWidget
from engine.widgets.ProjectManager import ProjectManager
from engine.widgets.PropertyObjectWidget import PropertyObjectWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.project_manager = ProjectManager()
        self.project_manager.open_project_signal.connect(self.load_project)

        self.__app = app
        self.__project = None

        self.setWindowTitle("Py-Live engine")
        self.setGeometry(100, 100, 1200, 800)

        if not self.project_manager.load():
            self.setCentralWidget(self.project_manager)
        else:
            self.init_ui()

    def init_ui(self):
        self.setMenuBar(QMenuBar())
        # Создаем главное меню
        menubar = self.menuBar()

        # Создаем меню "Файл" и добавляем кнопки
        project_menu = QMenu("Проект", self)
        menubar.addMenu(project_menu)

        # Вместо QAction добавляем кнопки
        new_button = QAction("Новый", self)
        open_button = QAction("Открыть", self)
        save_button = QAction("Сохранить", self)
        compile_button = QAction("Сборка", self)
        exit_button = QAction("Выход", self)

        # Обработчики для кнопок меню
        new_button.triggered.connect(self.new_file)
        open_button.triggered.connect(self.open_file)
        save_button.triggered.connect(self.save_file)
        exit_button.triggered.connect(self.close)

        project_menu.addAction(new_button)
        project_menu.addAction(open_button)
        project_menu.addAction(save_button)
        project_menu.addAction(compile_button)
        project_menu.addAction(exit_button)

        # Создаем меню "Справка"
        help_menu = QMenu("Справка", self)
        menubar.addMenu(help_menu)
        about_button = QAction("О программе", self)
        about_button.triggered.connect(self.about)
        help_menu.addAction(about_button)

        # Создаем центральный виджет и компоновку
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Файловый менеджер (снизу)
        self.file_manager = FileBrowser(self.__project.path_project)
        layout.addWidget(self.file_manager, 2, 1)

        # Свойства объекта (справа)
        self.property_widget = PropertyObjectWidget()
        layout.addWidget(self.property_widget, 0, 2, 0, 1)

        # Иерархия элементов (слева)
        self.hierarchy_widget = HierarchyWidget(self.property_widget)
        layout.addWidget(self.hierarchy_widget, 0, 0, 0, 1)

        # Окно Pygame (по центру)
        self.init_pygame_widget(layout)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(2, 1)

        self.setLayout(layout)

    def init_pygame_widget(self, layout):
        pass

    def new_file(self):
        self.project_manager.create_new_project()

    def open_file(self):
        self.project_manager.open_project()

    def save_file(self):
        print("Сохранение файла")

    def about(self):
        print("О программе")

    def load_project(self, project_path):
        self.__project = Project(project_path)
        self.init_ui()
        QMessageBox.information(self, "Project Loaded", f"Project opened: {project_path}")
