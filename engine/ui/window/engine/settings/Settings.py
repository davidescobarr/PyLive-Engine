from PySide6.QtWidgets import QLayout
from PySide6.QtCore import (QCoreApplication, QRect, Qt, QMetaObject, QSize)
from PySide6.QtGui import (QKeyEvent, QIcon)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea,
                               QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QLabel, QStackedWidget, QDialog)

from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
from engine.ui.widget.Engine.Settings.CurrentSceneSettings import CurrentSceneSettings
from engine.ui.widget.Engine.Settings.GeneralSettings import GeneralSettings
from engine.ui.widget.Engine.Settings.ScenesSettings import ScenesSettings
from engine.ui.widget.Engine.Settings.SettingGroup import ButtonQTreeWidgetItem


class Settings_UI(object):
    def __init__(self, project: Project, form, main_window):
        super().__init__()
        self.__settings_group = [GeneralSettings(project), ScenesSettings(project), CurrentSceneSettings(project)]
        self.setupUi(form, project, main_window)

    def setupUi(self, form, project: Project, main_window):
        if not form.objectName():
            form.setObjectName(u"Form")
        form.setFixedSize(640, 480)

        icon = QIcon()
        icon.addFile(u":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        form.setWindowIcon(icon)
        self.__main_window = main_window
        self.project = project
        self.gridLayoutWidget = QWidget(form)
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

        for group in self.__settings_group:
            group.setup_button(self.tree_widget)

        self.tree_widget.clicked.connect(self.open_setting_group)
        self.tree_grid.addWidget(self.tree_widget)
        self.main_grid.addLayout(self.tree_grid)
        # Создаем область прокрутки и QStackedWidget для вкладок настроек
        self.info_grid = QVBoxLayout()
        self.info_grid.setObjectName(u"info_grid")
        self.scrollArea_info_grid = QScrollArea(self.gridLayoutWidget)
        self.scrollArea_info_grid.setObjectName(u"scrollArea_info_grid")
        self.scrollArea_info_grid.setWidgetResizable(True)

        self.info_grid.addWidget(self.scrollArea_info_grid)
        self.main_grid.addLayout(self.info_grid)
        self.main_grid.setStretch(0, 2)
        self.main_grid.setStretch(1, 5)
        self.retranslateUi(form)
        QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(
            QCoreApplication.translate("Form", text_translator.get_translate("window.settings.title"), None))

    def open_setting_group(self, index):
        item = self.tree_widget.itemFromIndex(index)
        if isinstance(item, ButtonQTreeWidgetItem):
            # Создаем новый контентный виджет
            new_content_widget = QWidget()
            new_content_widget.setLayout(item.setting_group.layout)

            # Устанавливаем контентный виджет в QScrollArea
            self.scrollArea_info_grid.setWidget(new_content_widget)

class SettingsDialog(Settings_UI, QDialog):
    def __init__(self, project: Project, main_window):
        super().__init__(project, self, main_window)
        self.tree_widget.setFocusPolicy(Qt.StrongFocus)
        self.tree_widget.setFocus()