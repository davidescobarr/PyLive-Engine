from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
import sys

from engine.widgets.PropertyObjectWidget import PropertyObjectWidget


class HierarchyWidget(QWidget):
    def __init__(self, property_object_widget: PropertyObjectWidget):
        super().__init__()

        self.__property = property_object_widget
        self.initUI()

    def initUI(self):
        # Упаковываем в layout
        layout = QVBoxLayout(self)

        # Создаем QTreeWidget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Elements"])

        # Добавляем группы и элементы
        root = QTreeWidgetItem(self.tree, ["Root Group"])
        child_group_1 = QTreeWidgetItem(root, ["Child Group 1"])
        child_group_2 = QTreeWidgetItem(root, ["Child Group 2"])

        child_group_3 = QTreeWidgetItem(child_group_2, ["Child Group 2"])

        # Добавляем элементы в группы
        QTreeWidgetItem(child_group_1, ["Item 1"])
        QTreeWidgetItem(child_group_1, ["Item 2"])

        QTreeWidgetItem(child_group_2, ["Item 3"])
        QTreeWidgetItem(child_group_2, ["Item 4"])

        QTreeWidgetItem(child_group_3, ["Item 5"])

        # Устанавливаем иерархию
        self.tree.addTopLevelItem(root)

        # Добавляем выбор элемента
        self.tree.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.tree)

    def on_item_clicked(self, item, column):
        self.__property.set_text(item.text(column))