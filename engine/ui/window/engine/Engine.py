from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)
from PySide6.scripts.pyside_tool import project

import engine.ui.window.engine.Engine_rc
from engine.core.Project import Project
from engine.ui.widget.Engine.HierarchyWidget import HierarchyWidget
from engine.ui.window.engine.Engine_logic import Engine


class Engine_UI(object):
    def __init__(self, MainWindow, project: Project):
        self.project = project
        self.engine = Engine(project)
        self.setupUi(MainWindow)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(self.project.settings.name_project)
        MainWindow.resize(1200, 720)
        MainWindow.setMinimumSize(QSize(720, 520))
        MainWindow.setMaximumSize(QSize(16000, 16000))
        icon = QIcon()
        icon.addFile(u":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_save.triggered.connect(self.project.get_current_scene().save)
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_settings = QAction(MainWindow)
        self.action_settings.setObjectName(u"action_settings")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.hierarchy = QHBoxLayout()
        self.hierarchy_widget = HierarchyWidget(self.engine.project.get_current_scene())
        self.hierarchy.addWidget(self.hierarchy_widget)
        self.hierarchy.setObjectName(u"hierarchy")

        self.horizontalLayout_8.addLayout(self.hierarchy)

        self.main = QVBoxLayout()
        self.main.setObjectName(u"main")
        self.game = QVBoxLayout()
        self.game.setObjectName(u"game")

        self.main.addLayout(self.game)

        self.file_explorer = QVBoxLayout()
        self.file_explorer.setObjectName(u"file_explorer")

        self.main.addLayout(self.file_explorer)

        self.main.setStretch(0, 3)
        self.main.setStretch(1, 2)

        self.horizontalLayout_8.addLayout(self.main)

        self.properties = QHBoxLayout()
        self.properties.setObjectName(u"properties")

        self.horizontalLayout_8.addLayout(self.properties)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 3)
        self.horizontalLayout_8.setStretch(2, 1)

        self.horizontalLayout.addLayout(self.horizontalLayout_8)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.menu_project = QMenu(self.menubar)
        self.menu_project.setObjectName(u"menu_project")
        self.menu_about = QMenu(self.menubar)
        self.menu_about.setObjectName(u"menu_about")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_project.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())
        self.menu_project.addAction(self.action_settings)
        self.menu_project.addAction(self.action_save)
        self.menu_project.addAction(self.action_exit)
        self.menu_about.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", self.project.settings.name_project, None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430\u0446\u0438\u044f", None))
        self.menu_project.setTitle(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0435\u043a\u0442", None))
        self.menu_about.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi

