from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PropertyObjectWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__property_text = QLabel()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        layout.addWidget(self.__property_text)

        self.setLayout(layout)

    def set_text(self, text: str):
        self.__property_text.setText(text)