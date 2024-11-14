import copy

from PySide6.QtWidgets import (
    QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QMessageBox, QMenu, QInputDialog
)
from PySide6.QtCore import Qt, QTimer, QMimeData
from PySide6.QtGui import QIcon, QPalette, QColor, QDragEnterEvent, QDropEvent
from core.Scene import Scene
from core.objects.Object import Object
from core.scene.SceneComponent import SceneComponent
from core.scene.components.Group import Group
from core.scene.components.Object import SceneObject
from core.utils.ClassLoader import load_class_from_file
from core.utils.delegates.PropertyValueDelegate import property_value_delegate, DelegateNotifier
from engine.ui.lang.TextTranslater import text_translator


class HierarchyItem(QTreeWidgetItem):
    """Class to represent a hierarchy item."""

    def __init__(self, scene_component: SceneComponent):
        super().__init__([scene_component.name])
        self.object = scene_component
        property_value_delegate.subscribe(self.update_name)

    def update_name(self, func):
        """Update item name when it is changed in the property editor."""
        if not self.object.name or not isinstance(self.object, SceneObject):
            return
        if self.object.object.__class__.name == func:
            self.setText(0, self.object.name)


class FolderItem(HierarchyItem):
    """Class to represent a folder in the hierarchy."""

    def __init__(self, group: Group):
        super().__init__(group)
        self.setFlags(self.flags() | Qt.ItemIsDropEnabled)
        self.setIcon(0, QIcon('icons/folder_icon.png'))  # Установить иконку для папки


class ObjectItem(HierarchyItem):
    """Class to represent an object in the hierarchy."""

    def __init__(self, scene_object: SceneObject):
        super().__init__(scene_object)
        self.setFlags(self.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsDragEnabled)
        self.setIcon(0, QIcon('icons/object_icon.png'))  # Установить иконку для объекта


class HierarchyWidget(QTreeWidget):
    """Widget to display the scene hierarchy."""

    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.setColumnCount(1)
        self.setHeaderLabels([scene.name])
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setAcceptDrops(True)  # Разрешить прием дропа
        self.init_scene_hierarchy()
        self.itemClicked.connect(self.item_click)
        self.func_by_item_click = None
        self.__notifier_by_update_object = DelegateNotifier()
        self.scene.set_notify_for_change_name(self.change_name_scene)

    def subscribe_by_update_object(self, func: callable):
        self.__notifier_by_update_object.subscribe(func)

    def change_name_scene(self):
        self.setHeaderLabels([self.scene.name])

    def subscribe_by_item_choose(self, func):
        self.func_by_item_click = func

    def item_click(self, item):
        if isinstance(item, HierarchyItem) and self.func_by_item_click:
            self.func_by_item_click(item.object)

    def init_scene_hierarchy(self):
        """Initialize the scene hierarchy."""
        self.clear()
        if not self.scene:
            return
        for obj in self.scene.main_group.get_objects():
            if isinstance(obj, SceneObject):
                self.addTopLevelItem(self.new_object(obj))
            elif isinstance(obj, Group):
                self.addTopLevelItem(self.new_group(obj))
        self.expandAll()

    def new_group(self, group: Group) -> FolderItem:
        folder = FolderItem(group)
        for obj in group.get_objects():
            if isinstance(obj, SceneObject):
                folder.addChild(self.new_object(obj))
            elif isinstance(obj, Group):
                folder.addChild(self.new_group(obj))
        return folder

    def new_object(self, obj: SceneObject) -> ObjectItem:
        return ObjectItem(obj)

    def dropEvent(self, event: QDropEvent) -> None:
        source_item = self.currentItem()
        if not isinstance(source_item, HierarchyItem):
            super().dropEvent(event)
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    file_path = url.toLocalFile()
                    if file_path.endswith(".py"):
                        target_item = self.itemAt(event.position().toPoint())
                        if target_item:
                            target_object = target_item.object
                            if isinstance(target_object, SceneObject):
                                self.handle_python_file_drop(file_path, url.fileName(), target_object)
            return
        if source_item.parent():
            parent_item = source_item.parent()
            if isinstance(parent_item, FolderItem):
                parent_item.object.remove_object(parent_item.indexOfChild(source_item))
        else:
            self.scene.main_group.remove_object(self.indexOfTopLevelItem(source_item))
        super().dropEvent(event)
        if source_item.parent():
            parent_item = source_item.parent()
            if isinstance(parent_item, FolderItem):
                source_item.object.order = parent_item.indexOfChild(source_item)
                parent_item.object.add_object(source_item.object)
        else:
            source_item.object.order = self.indexOfTopLevelItem(source_item)
            self.scene.main_group.add_object(source_item.object)
        self.reload_hierarchy()

    def handle_python_file_drop(self, file_path, file_name, target_object):
        load_object = load_class_from_file(file_path, file_name.removesuffix(".py"))
        if load_object:
            if isinstance(load_object, Object):
                # Создаем глубокую копию старого объекта
                old_object_copy = copy.deepcopy(target_object.object)

                # Меняем класс объекта и инициализируем его
                target_object.object.__class__ = load_object.__class__
                target_object.object.__init__()

                # Копируем поля из старого объекта в новый
                target_object.object.copy_fields(old_object_copy)

                self.__notifier_by_update_object.notify()
                print("Successfully changed class and copied fields")
            else:
                print("Class object not extends base class Object! engine.ui.widget.Engine.HierarchyWidget.py:100")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            return event.acceptProposedAction()
        return super().dragEnterEvent(event)

    def rename_item(self, item: HierarchyItem, name: str):
        """Rename the specified item."""
        item.setText(0, name)
        item.object.name = name

    def delete_item(self, item: HierarchyItem):
        """Delete the specified item."""
        parent = item.parent()
        order = 0
        if parent:
            order = parent.indexOfChild(item)
            parent.removeChild(item)
        else:
            order = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(order)
        if isinstance(parent, FolderItem):
            parent.object.remove_object(order)
        else:
            self.scene.main_group.remove_object(order)

        self.reload_hierarchy()

    def create_folder(self):
        """Create a new folder."""
        new_group = Group(self.scene, "group", -1)
        self.scene.main_group.add_object(new_group)
        self.addTopLevelItem(self.new_group(new_group))
        self.reload_hierarchy()

    def create_object(self):
        """Create a new object."""
        obj = Object()
        obj.name = "object"
        new_object = SceneObject(self.scene, obj, -1)
        self.scene.main_group.add_object(new_object)
        self.addTopLevelItem(self.new_object(new_object))
        self.reload_hierarchy()

    def reload_hierarchy(self):
        self.scene.save()
        self.scene.load_objects()
        self.init_scene_hierarchy()

    def empty_click_context_menu(self, context_menu: QMenu, event):
        """Context menu for clicking on empty space."""
        create_folder_action = context_menu.addAction(
            text_translator.get_translate("window.engine.hierarchy.button.create_folder"))
        create_object_action = context_menu.addAction(
            text_translator.get_translate("window.engine.hierarchy.button.create_object"))
        action = context_menu.exec(event.globalPos())
        if action == create_folder_action:
            self.create_folder()
        elif action == create_object_action:
            self.create_object()

    def click_by_object_context_menu(self, context_menu: QMenu, event, item: HierarchyItem):
        """Context menu for clicking on an object."""
        rename_action = context_menu.addAction(text_translator.get_translate("window.engine.hierarchy.object.rename"))
        delete_action = context_menu.addAction(text_translator.get_translate("window.engine.hierarchy.object.delete"))
        action = context_menu.exec(event.globalPos())
        if action == rename_action:
            new_name, ok = QInputDialog.getText(self,
                                                text_translator.get_translate("window.engine.hierarchy.rename.title"),
                                                text_translator.get_translate(
                                                    "window.engine.hierarchy.rename.new_name"))
            if ok and new_name:
                self.rename_item(item, new_name)
        elif action == delete_action:
            reply = QMessageBox.question(self, text_translator.get_translate("window.engine.hierarchy.delete.title"),
                                         f"{text_translator.get_translate('window.engine.hierarchy.delete.describe')} {item.text(0)}?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_item(item)

    def contextMenuEvent(self, event):
        """Handle context menu event."""
        item = self.itemAt(event.pos())
        context_menu = QMenu(self)
        if item is None:
            self.empty_click_context_menu(context_menu, event)
        elif isinstance(item, HierarchyItem):
            self.click_by_object_context_menu(context_menu, event, item)