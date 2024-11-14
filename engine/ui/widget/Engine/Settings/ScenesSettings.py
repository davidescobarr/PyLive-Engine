from typing import override

from PySide6.QtCore import QRect
from PySide6.QtWidgets import (QWidget, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QFormLayout, QMessageBox, QGridLayout, QScrollArea, QListWidget, QLayout,
                               QListWidgetItem)

from core.Scene import Scene
from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
from engine.ui.widget.Engine.Settings.SettingGroup import SettingGroup


class SceneObject(QListWidgetItem):
    def __init__(self, scene: Scene):
        self.__scene = scene
        super().__init__(scene.name)

    @property
    def scene(self) -> Scene:
        return self.__scene

class ScenesSettings(SettingGroup):
    def __init__(self, project: Project):
        self.project = project
        self.settings = project.settings

        super().__init__(project, "window.settings.scenes.button.name")

    def setup_main_layout(self) -> QLayout:
        self.main_grid = QGridLayout()
        self.main_grid.setObjectName(u"main_grid")
        self.main_grid.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")

        self.scene_up_button = QPushButton()
        self.scene_up_button.setObjectName(u"scene_up_button")
        self.scene_up_button.setText(text_translator.get_translate("window.settings.scenes.button.scene_up"))

        self.scene_up_button.clicked.connect(self.move_scene_up)

        self.buttons_layout.addWidget(self.scene_up_button)

        self.scene_down_button = QPushButton()
        self.scene_down_button.setObjectName(u"scene_down_button")
        self.scene_down_button.setText(text_translator.get_translate("window.settings.scenes.button.scene_down"))

        self.scene_down_button.clicked.connect(self.move_scene_down)

        self.buttons_layout.addWidget(self.scene_down_button)

        self.choose_button = QPushButton()
        self.choose_button.setObjectName(u"choose_button")
        self.choose_button.setText(text_translator.get_translate("window.settings.scenes.button.choose"))
        self.choose_button.clicked.connect(self.load_scene_button_pressed)

        self.buttons_layout.addWidget(self.choose_button)

        self.delete_button = QPushButton()
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setText(text_translator.get_translate("window.settings.scenes.button.delete"))
        self.delete_button.clicked.connect(self.press_delete_button_pressed)

        self.buttons_layout.addWidget(self.delete_button)

        self.create_button = QPushButton()
        self.create_button.setObjectName(u"create_button")
        self.create_button.setText(text_translator.get_translate("window.settings.scenes.button.create"))

        self.create_button.clicked.connect(self.create_new_scene)

        self.buttons_layout.addWidget(self.create_button)

        self.main_grid.addLayout(self.buttons_layout, 1, 0, 1, 1)

        self.scrollArea_scenes = QScrollArea()
        self.scrollArea_scenes.setObjectName(u"scrollArea_scenes")
        self.scrollArea_scenes.setWidgetResizable(True)
        self.scrollAreaScenesContents = QWidget()
        self.scrollAreaScenesContents.setObjectName(u"scrollAreaScenesContents")
        self.scrollAreaScenesContents.setGeometry(QRect(0, 0, 437, 425))
        self.scenes_list = QListWidget(self.scrollAreaScenesContents)
        self.scenes_list.setObjectName(u"scenes_list")
        self.scenes_list.setGeometry(QRect(0, 0, 471, 451))

        self.init_scenes()

        self.scrollArea_scenes.setWidget(self.scrollAreaScenesContents)

        self.main_grid.addWidget(self.scrollArea_scenes, 0, 0, 1, 1)

        self.main_grid.setRowStretch(0, 10)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.main_grid)

        return main_layout

    def press_delete_button_pressed(self):
        item = self.scenes_list.currentItem()

        if isinstance(item, SceneObject):
            self.delete_scene(item)

    def delete_scene(self, scene_object: SceneObject):
        self.project.delete_scene(scene_object.scene)
        self.scenes_list.takeItem(self.scenes_list.row(scene_object))

    def move_scene_up(self):
        item = self.scenes_list.currentItem()

        if isinstance(item, SceneObject):
            scene = item.scene

            if scene.order_load != 0:
                self.project.get_scenes()[scene.order_load - 1].order_load = scene.order_load
                scene.order_load -= 1
                self.project.reorder_scenes()
                self.init_scenes()

    def move_scene_down(self):
        item = self.scenes_list.currentItem()

        if isinstance(item, SceneObject):
            scene = item.scene

            if scene.order_load != len(self.project.get_scenes()) - 1:
                self.project.get_scenes()[scene.order_load + 1].order_load = scene.order_load
                scene.order_load += 1
                self.project.reorder_scenes()
                self.init_scenes()

    def init_scenes(self):
        self.scenes_list.clear()

        for scene in self.project.get_scenes():
            self.scenes_list.addItem(SceneObject(scene))

    def load_scene_button_pressed(self):
        item = self.scenes_list.currentItem()

        if isinstance(item, SceneObject):
            self.load_scene(item.scene)

    def load_scene(self, scene: Scene):
        self.project.init_scene(scene, dev=True)

    def create_new_scene(self):
        name = "New Scene"
        i = 1
        while self.project.get_scene_by_name(name):
            name = f"New Scene ({i})"
            i += 1
        self.project.create_new_scene(name)
        self.init_scenes()