from PySide6.QtCore import (QCoreApplication, QRect, Qt, QMetaObject, QSize)
from PySide6.QtGui import (QKeyEvent, QIcon)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea,
                               QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QStackedWidget, QDialog)

from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
import engine.ui.window.engine.Engine_rc
from engine.ui.widget.Engine.Settings.GeneralSettings import GeneralSettings


class Settings_UI(object):
    def setupUi(self, Form, project: Project, MainWindow):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setFixedSize(640, 480)

        icon = QIcon()
        icon.addFile(u":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.MainWindow = MainWindow
        self.project = project
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 641, 481))
        self.main_grid = QHBoxLayout(self.gridLayoutWidget)
        self.main_grid.setObjectName(u"main_grid")
        self.main_grid.setContentsMargins(0, 0, 0, 0)
        # Создаем и настраиваем дерево виджетов
        self.tree_grid = QVBoxLayout()
        self.tree_grid.setObjectName(u"tree_grid")
        self.tree_widget = QTreeWidget(self.gridLayoutWidget)
        self.tree_widget.setObjectName(u"tree_widget")
        # Добавляем элементы в дерево
        self.tree_widget.setHeaderHidden(True)
        for setting in ['General', 'Scenes']:
            item = QTreeWidgetItem(self.tree_widget)
            item.setText(0, QCoreApplication.translate("Form", setting, None))
        self.tree_widget.clicked.connect(self.change_setting)
        self.tree_grid.addWidget(self.tree_widget)
        self.main_grid.addLayout(self.tree_grid)
        # Создаем область прокрутки и QStackedWidget для вкладок настроек
        self.info_grid = QVBoxLayout()
        self.info_grid.setObjectName(u"info_grid")
        self.scrollArea_info_grid = QScrollArea(self.gridLayoutWidget)
        self.scrollArea_info_grid.setObjectName(u"scrollArea_info_grid")
        self.scrollArea_info_grid.setWidgetResizable(True)
        self.stacked_widget = QStackedWidget()
        # Добавляем примерные страницы настроек
        self.general_settings_page = GeneralSettings(project.settings)
        self.stacked_widget.addWidget(self.general_settings_page)
        self.scenes_settings_page = QWidget()
        self.scenes_settings_page_layout = QVBoxLayout(self.scenes_settings_page)
        self.label_display = QLabel("Scenes Settings")
        self.scenes_settings_page_layout.addWidget(self.label_display)
        self.stacked_widget.addWidget(self.scenes_settings_page)
        self.scrollArea_info_grid.setWidget(self.stacked_widget)
        self.info_grid.addWidget(self.scrollArea_info_grid)
        self.main_grid.addLayout(self.info_grid)
        self.main_grid.setStretch(0, 2)
        self.main_grid.setStretch(1, 5)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(
            QCoreApplication.translate("Form", text_translator.get_translate("window.settings.title"), None))

    # Слот для изменения вкладок настроек
    def change_setting(self, index):
        self.stacked_widget.setCurrentIndex(index.row())
        self.project.init_current_scene(self.project.get_scenes()[1])
        self.project.get_current_scene().dev = True
        self.MainWindow.initialize_sections()


class SettingsDialog(QDialog, Settings_UI):
    def __init__(self, project: Project, MainWindow):
        super(SettingsDialog, self).__init__()
        self.setupUi(self, project, MainWindow)
        self.tree_widget.setFocusPolicy(Qt.StrongFocus)
        self.tree_widget.setFocus()