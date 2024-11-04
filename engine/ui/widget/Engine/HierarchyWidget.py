from PySide6.QtWidgets import (
    QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QMessageBox, QMenu, QInputDialog
)
from PySide6.QtCore import Qt

from core.Scene import Scene
from core.objects.Object import Object
from core.scene.SceneComponent import SceneComponent
from core.scene.components.Group import Group
from core.scene.components.Object import SceneObject

class HierarchyItem(QTreeWidgetItem):
    def __init__(self, object: SceneComponent):
        super().__init__([object.name])
        self.object = object

class FolderItem(HierarchyItem):
    def __init__(self, group: Group):
        super().__init__(group)
        self.setFlags(self.flags() | Qt.ItemIsDropEnabled)  # Папка поддерживает drop


class ObjectItem(HierarchyItem):
    def __init__(self, object: SceneObject):
        super().__init__(object)
        # Файл не поддерживает drop, но оставляем возможность перемещаться внутри родительской папки
        self.setFlags(self.flags() & ~Qt.ItemIsDropEnabled | Qt.ItemIsDragEnabled)

class HierarchyWidget(QTreeWidget):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.setColumnCount(1)
        self.setHeaderLabels([scene.name])
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.init_scene_hierarchy()

    def init_scene_hierarchy(self):
        if not self.scene:
            return

        for object in self.scene.main_group.get_objects():
            if isinstance(object, SceneObject):
                self.addTopLevelItem(self.new_object(object))
            if isinstance(object, Group):
                self.addTopLevelItem(self.new_group(object))

        self.expandAll()

    def new_group(self, group: Group) -> FolderItem:
        folder = FolderItem(group)

        for object in group.get_objects():
            if isinstance(object, SceneObject):
                folder.addChild(self.new_object(object))
            if isinstance(object, Group):
                folder.addChild(self.new_group(object))

        return folder

    def new_object(self, object: SceneObject) -> ObjectItem:
        return ObjectItem(object)

    def dropEvent(self, event):
        source_item = self.currentItem()

        if not isinstance(source_item, HierarchyItem):
            super().dropEvent(event)
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

        self.scene.update()

    def rename_item(self, item: HierarchyItem, name: str):
        item.setText(0, name)
        item.object.name = name

    def delete_item(self, item: HierarchyItem):
        parent = item.parent()
        order = 0

        if parent:
            order = parent.indexOfChild(item)
            parent.removeChild(item)
        else:
            order = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))

        if isinstance(parent, FolderItem):
            parent.object.remove_object(order)
        else:
            self.scene.main_group.remove_object(order)

    def create_folder(self):
        new_group = Group(self.scene, "group", -1)
        self.scene.main_group.add_object(new_group)
        self.addTopLevelItem(self.new_group(new_group))

    def create_object(self):
        object = Object()
        object.name = "object"
        new_object = SceneObject(self.scene, object, -1)
        self.scene.main_group.add_object(new_object)
        self.addTopLevelItem(self.new_object(new_object))

    def empty_click_context_menu(self, context_menu: QMenu, event):
        create_folder_action = context_menu.addAction("Создать папку")
        create_object_action = context_menu.addAction("Создать объект")

        action = context_menu.exec(event.globalPos())

        if action == create_folder_action:
            self.create_folder()

        elif action == create_object_action:
            self.create_object()

    def click_by_object_context_menu(self, context_menu: QMenu, event, item: HierarchyItem):
        rename_action = context_menu.addAction("Изменить название")
        delete_action = context_menu.addAction("Удалить")

        action = context_menu.exec(event.globalPos())

        if action == rename_action:
            new_name, ok = QInputDialog.getText(self, "Изменить название", "Новое название:")
            if ok and new_name:
                self.rename_item(item, new_name)

        elif action == delete_action:
            reply = QMessageBox.question(self, "Подтвердите удаление", f"Удалить {item.text(0)}?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.delete_item(item)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())

        context_menu = QMenu(self)

        if item is None:
            self.empty_click_context_menu(context_menu, event)

            return

        if not isinstance(item, HierarchyItem):
            return

        self.click_by_object_context_menu(context_menu, event, item)