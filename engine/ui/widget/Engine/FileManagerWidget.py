from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QVBoxLayout, QWidget, QMenu, \
    QMessageBox, QFileDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import QDir, QModelIndex, Qt
import os
import shutil
import subprocess


class FileManagerWidget(QWidget):
    def __init__(self, default_path=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(default_path if default_path else QDir.rootPath()))
        self.tree.setSortingEnabled(True)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDragDropMode(QTreeView.InternalMove)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

    def open_context_menu(self, position):
        indexes = self.tree.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            file_path = self.model.filePath(index)
            context_menu = QMenu()
            context_menu.addAction(self.create_action("Open", lambda: self.open_file(file_path)))
            context_menu.addAction(self.create_action("Open With...", lambda: self.open_file_with(file_path)))
            context_menu.addAction(self.create_action("Create File", lambda: self.create_file(file_path)))
            context_menu.addAction(self.create_action("Rename", lambda: self.rename_file(file_path)))
            context_menu.addAction(self.create_action("Delete", lambda: self.delete_file(file_path)))
            context_menu.exec(self.tree.viewport().mapToGlobal(position))

    def create_action(self, name, method):
        action = QAction(name, self)
        action.triggered.connect(method)
        return action

    def open_file(self, file_path):
        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")

    def open_file_with(self, file_path):
        if os.path.isfile(file_path):
            program, _ = QFileDialog.getOpenFileName(self, "Open With...", QDir.homePath(),
                                                     "Executables (*.exe);;All Files (*)")
            if program:
                try:
                    subprocess.Popen([program, file_path])
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to open file with {program}.\n{str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "Selected item is not a file.")

    def create_file(self, dir_path):
        if not os.path.isdir(dir_path):
            dir_path = os.path.dirname(dir_path)
        new_file_path, _ = QFileDialog.getSaveFileName(self, "Create File", dir_path)
        if new_file_path:
            open(new_file_path, 'w').close()
            self.refresh_model()

    def rename_file(self, file_path):
        if os.path.exists(file_path):
            new_file_path, _ = QFileDialog.getSaveFileName(self, "Rename File", os.path.dirname(file_path))
            if new_file_path:
                os.rename(file_path, new_file_path)
                self.refresh_model()

    def delete_file(self, file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path) if os.path.isfile(file_path) else shutil.rmtree(file_path)
                self.refresh_model()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def refresh_model(self):
        self.model.setRootPath(QDir.rootPath())