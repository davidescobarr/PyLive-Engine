from PyQt6.QtGui import QFileSystemModel, QDesktopServices, QAction
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTreeView, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QHeaderView, QMessageBox, QInputDialog, QMenu
)
from PyQt6.QtCore import QDir, Qt, QUrl, QPoint
import sys
import os

class FileBrowser(QWidget):
    def __init__(self, root_dir: str):
        super().__init__()
        self.root_dir = root_dir  # Укажите желаемую директорию
        self.current_dir = self.root_dir
        self.initUI()

    def initUI(self):
        # Основная компоновка
        layout = QVBoxLayout(self)

        # Виджет файлового дерева
        self.file_tree = QTreeView(self)
        layout.addWidget(self.file_tree)

        # Модель файловой системы
        self.model = QFileSystemModel()
        self.model.setRootPath(self.root_dir)
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.file_tree.setModel(self.model)

        # Настройки отображения
        self.file_tree.setRootIndex(self.model.index(self.root_dir))
        self.file_tree.setSortingEnabled(True)
        self.file_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Подключение сигналов
        self.file_tree.clicked.connect(self.onFileClicked)
        self.file_tree.doubleClicked.connect(self.openFileOnDoubleClick)
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.openContextMenu)

        # Отображение информации о выбранном файле
        self.file_info_label = QLabel("Select a file to see info", self)
        layout.addWidget(self.file_info_label)

    def goBack(self):
        # Перейти к предыдущей папке
        current_path = QDir(self.current_dir).absolutePath()
        parent_path = QDir(current_path).absolutePath() if current_path != self.root_dir else self.root_dir
        self.current_dir = parent_path
        self.file_tree.setRootIndex(self.model.index(self.current_dir))

    def createFile(self):
        # Создать новый файл
        file_name, _ = QInputDialog.getText(self, "Create File", "Enter file name:")
        if file_name:
            file_path = os.path.join(self.current_dir, file_name)
            try:
                with open(file_path, 'w') as f:
                    f.write("")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create file: {e}")

    def deleteFile(self):
        # Удалить выбранный файл
        index = self.file_tree.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Warning", "Please select a file to delete.")
            return

        file_path = self.model.filePath(index)
        if QMessageBox.question(self, "Delete File", f"Are you sure you want to delete '{file_path}'?") == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path) if os.path.isfile(file_path) else os.rmdir(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete file: {e}")

    def createFolder(self):
        # Создать новую папку
        folder_name, _ = QInputDialog.getText(self, "Create Folder", "Enter folder name:")
        if folder_name:
            folder_path = os.path.join(self.current_dir, folder_name)
            try:
                os.mkdir(folder_path)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not create folder: {e}")

    def openFile(self):
        # Открыть файл в стороннем приложении
        index = self.file_tree.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Warning", "Please select a file to open.")
            return

        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")

    def openFileOnDoubleClick(self, index):
        # Открытие файла по двойному клику
        file_path = self.model.filePath(index)
        if os.path.isfile(file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def openContextMenu(self, position):
        # Создание контекстного меню
        menu = QMenu()

        # Пункты меню
        open_action = QAction("Open", self)
        delete_action = QAction("Delete", self)
        create_file_action = QAction("Create File", self)
        create_folder_action = QAction("Create Folder", self)

        # Добавление пунктов в меню
        index = self.file_tree.indexAt(position)
        if index.isValid():
            menu.addAction(open_action)
            menu.addAction(delete_action)
        menu.addAction(create_file_action)
        menu.addAction(create_folder_action)

        # Подключение действий
        open_action.triggered.connect(self.openFile)
        delete_action.triggered.connect(self.deleteFile)
        create_file_action.triggered.connect(self.createFile)
        create_folder_action.triggered.connect(self.createFolder)

        # Отображение меню
        menu.exec(self.file_tree.viewport().mapToGlobal(position))

    def onFileClicked(self, index):
        # Обработчик клика по файлу, отображает путь и размер файла
        file_path = self.model.filePath(index)
        file_info = f"Selected: {file_path}"
        if self.model.isDir(index):
            file_info += " (directory)"
            self.current_dir = file_path
        else:
            file_size = self.model.size(index)
            file_info += f" (file, {file_size} bytes)"
        self.file_info_label.setText(file_info)