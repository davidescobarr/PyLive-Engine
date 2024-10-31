import sys

from PyQt6.QtWidgets import QApplication

from engine.MainWindow import MainWindow

import engine.main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())