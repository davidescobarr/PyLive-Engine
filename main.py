import sys

from PySide6.QtWidgets import QMainWindow, QApplication

from engine.ui.window.project_manager.ProjectManager import ProjectManager_UI

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ProjectManager_UI(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())