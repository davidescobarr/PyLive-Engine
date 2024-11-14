from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QLayout

from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator


class ButtonQTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, setting_group, parent=None):
        super().__init__(parent)
        self.__setting_group = setting_group

    @property
    def setting_group(self):
        return self.__setting_group

class SettingGroup:
    def __init__(self, project: Project, translate_key_button: str = ""):
        self.__project = project
        self.__layout = self.setup_main_layout()
        self.__button = None
        self.__translate_key_button = translate_key_button

    def setup_main_layout(self) -> QLayout:
        pass

    def setup_button(self, tree: QTreeWidget) -> ButtonQTreeWidgetItem:
        item = ButtonQTreeWidgetItem(setting_group=self, parent=tree)
        item.setText(0, text_translator.get_translate(self.__translate_key_button))
        self.__button = item
        return item

    @property
    def button(self):
        return self.__button

    @property
    def layout(self) -> QLayout:
        return self.setup_main_layout()