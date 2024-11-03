from datetime import datetime

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt, QAbstractTableModel)
from PySide6.QtGui import (QCursor,
                           QFont, QIcon,
                           QPixmap)
from PySide6.QtWidgets import (QFrame, QGridLayout, QGroupBox,
                               QHeaderView, QLabel, QPushButton,
                               QScrollArea, QSizePolicy, QTableView, QWidget, QStyledItemDelegate, QDialog, QLineEdit,
                               QFileDialog, QMessageBox, QVBoxLayout)
from engine.core.Loader import Loader
from engine.ui.window.project_manager.ProjectManager_logic import LastProject, Projects


class ProjectViewer(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def rowCount(self, parent= ...):
        return len(self.items)

    def columnCount(self, parent= ...):
        return 3

    def data(self, index, role = ...):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            project = self.items[index.row()]
            if index.column() == 0:
                return project['name']
            elif index.column() == 1:
                return project['version']
            elif index.column() == 2:
                return project['last_open']
        return None

    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                name = {
                    0: "Project name",
                    1: "Engine version",
                    2: "Last open"
                }.get(section)

                return name

class ProjectDialog(QDialog):
    def __init__(self, loader: Loader, projects: Projects):
        super().__init__()
        self.loader = loader
        self.projects = projects

        self.setWindowTitle("Создание нового проекта")

        # Поле для ввода названия проекта
        self.name_label = QLabel("Название проекта:")
        self.name_input = QLineEdit()

        # Поле для выбора пути
        self.path_label = QLabel("Путь до папки проекта:")
        self.path_input = QLineEdit()
        self.path_button = QPushButton("Выбрать путь")
        self.path_button.clicked.connect(self.select_path)

        # Кнопка для создания проекта
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.create_project)

        # Вертикальное расположение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.path_button)
        layout.addWidget(self.create_button)
        self.setLayout(layout)

    def select_path(self):
        # Открываем диалог выбора папки
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для проекта")
        if folder_path:
            self.path_input.setText(folder_path)

    def create_project(self):
        # Получаем название и путь
        project_name = self.name_input.text()
        project_path = self.path_input.text()

        # Проверка заполненности полей
        if not project_name or not project_path:
            QMessageBox.warning(self, "Ошибка", "Введите название и путь до папки проекта")
            return

        project = self.loader.create_project(project_path, project_name)
        self.projects.add_new_project(LastProject(project.settings.name_project, project_path, project.settings.version_engine, datetime.today().today().date().isoformat()))
        self.accept()

class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, func, model, projects: Projects, parent=None):
        super().__init__(parent)
        self.func = func
        self.model = model
        self.projects = projects

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:
            # Call the function to open the project
            self.projects.get_last_projects()[index.row()].last_open = datetime.today().date().isoformat()
            self.projects.save()
            self.func(self.model.items[index.row()]["path"])
            return True
        return super().editorEvent(event, model, option, index)

class ProjectManager_UI(object):
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)

        self.projects = Projects()
        self.loader = Loader(MainWindow)
        self.model = ProjectViewer()
        self.model.setItems(self.projects.get_formatted_last_projects())
        self.table_projects_3.setModel(self.model)
        self.table_projects_3.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_projects_3.horizontalHeader().setFixedSize(651, 30)
        self.table_projects_3.setFixedWidth(651)
        self.table_projects_3.verticalHeader().setVisible(False)
        self.table_projects_3.setSelectionBehavior(QTableView.SelectRows)
        self.table_projects_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.table_projects_3.setItemDelegate(ButtonDelegate(self.loader.load_engine, self.model, self.projects))

    def create_project_dialog(self):
        dialog = ProjectDialog(self.loader, self.projects)
        dialog.exec()
        self.model.setItems(self.projects.get_formatted_last_projects())

    def open_project(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Выберите папку проекта")
        if folder_path:
            project = self.loader.open_project(folder_path)

            if project:
                self.projects.add_new_project(
                    LastProject(project.settings.name_project, folder_path, project.settings.version_engine,
                                datetime.today().date().isoformat()))
                self.model.setItems(self.projects.get_formatted_last_projects())
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный путь до проекта")

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 560)
        MainWindow.setMinimumSize(QSize(900, 560))
        MainWindow.setMaximumSize(QSize(900, 560))
        icon = QIcon()
        icon.addFile(u":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 901, 561))
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(25)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.header_3 = QGroupBox(self.layoutWidget)
        self.header_3.setObjectName(u"header_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_3.sizePolicy().hasHeightForWidth())
        self.header_3.setSizePolicy(sizePolicy)
        self.header_3.setMinimumSize(QSize(0, 50))
        self.header_3.setStyleSheet(u"background-color: #fff;\n"
"border: none;")
        self.logo_icon_3 = QLabel(self.header_3)
        self.logo_icon_3.setObjectName(u"logo_icon_3")
        self.logo_icon_3.setGeometry(QRect(10, 5, 40, 40))
        self.logo_icon_3.setMinimumSize(QSize(0, 40))
        self.logo_icon_3.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.logo_icon_3.setPixmap(QPixmap(u":/icon/snake.png"))
        self.logo_icon_3.setScaledContents(True)
        self.logo_icon_3.setWordWrap(False)
        self.logo_text_3 = QLabel(self.header_3)
        self.logo_text_3.setObjectName(u"logo_text_3")
        self.logo_text_3.setGeometry(QRect(60, 0, 101, 50))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo_text_3.sizePolicy().hasHeightForWidth())
        self.logo_text_3.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies([u"Microsoft JhengHei Light"])
        font.setPointSize(12)
        self.logo_text_3.setFont(font)
        self.logo_text_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.version_3 = QLabel(self.header_3)
        self.version_3.setObjectName(u"version_3")
        self.version_3.setGeometry(QRect(800, 0, 91, 50))
        sizePolicy1.setHeightForWidth(self.version_3.sizePolicy().hasHeightForWidth())
        self.version_3.setSizePolicy(sizePolicy1)
        self.version_3.setFont(font)
        self.version_3.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.version_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.header_3, 0, 0, 1, 1)

        self.main_3 = QGroupBox(self.layoutWidget)
        self.main_3.setObjectName(u"main_3")
        self.main_3.setStyleSheet(u"border: none;")
        self.buttons_3 = QScrollArea(self.main_3)
        self.buttons_3.setObjectName(u"buttons_3")
        self.buttons_3.setGeometry(QRect(0, -11, 211, 491))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttons_3.sizePolicy().hasHeightForWidth())
        self.buttons_3.setSizePolicy(sizePolicy2)
        self.buttons_3.setStyleSheet(u"border: none;")
        self.buttons_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 211, 491))
        self.projects_3 = QPushButton(self.scrollAreaWidgetContents_3)
        self.projects_3.setObjectName(u"projects_3")
        self.projects_3.setGeometry(QRect(0, 10, 211, 30))
        self.projects_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.projects_3.setStyleSheet(u"QPushButton\n"
"{\n"
"   background-color: transparent;\n"
"	border: none;\n"
"	font-size: 14px;\n"
"	text-align: left;\n"
"	padding-left: 15px;\n"
"	border-left: 3px solid blue;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   background-color:white;\n"
"	cursor: pointer;\n"
"}")
        self.buttons_3.setWidget(self.scrollAreaWidgetContents_3)
        self.project_choose_3 = QGroupBox(self.main_3)
        self.project_choose_3.setObjectName(u"project_choose_3")
        self.project_choose_3.setGeometry(QRect(220, 0, 671, 471))
        self.project_choose_3.setStyleSheet(u"border: none;")
        self.text_3 = QLabel(self.project_choose_3)
        self.text_3.setObjectName(u"text_3")
        self.text_3.setGeometry(QRect(10, 10, 81, 16))
        font1 = QFont()
        font1.setFamilies([u"Trebuchet MS"])
        font1.setPointSize(16)
        self.text_3.setFont(font1)
        self.pushButton_5 = QPushButton(self.project_choose_3)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(464, 10, 91, 24))
        font2 = QFont()
        font2.setFamilies([u"Verdana"])
        self.pushButton_5.setFont(font2)
        self.pushButton_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_5.clicked.connect(self.open_project)
        self.pushButton_5.setStyleSheet(u"QPushButton\n"
"{\n"
"   background-color: white;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   	background-color: #cccccc;\n"
"}")
        self.pushButton_6 = QPushButton(self.project_choose_3)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(570, 10, 91, 24))
        self.pushButton_6.setFont(font2)
        self.pushButton_6.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_6.clicked.connect(self.create_project_dialog)
        self.pushButton_6.setStyleSheet(u"QPushButton\n"
"{\n"
"   background-color: #55aaff;\n"
"	border: none;\n"
"	color: #fff;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   	background-color: #4387ca;\n"
"}")
        self.table_projects_3 = QTableView(self.project_choose_3)
        self.table_projects_3.setObjectName(u"table_projects_3")
        self.table_projects_3.setGeometry(QRect(10, 40, 651, 421))
        self.table_projects_3.setFrameShape(QFrame.Shape.Box)
        self.table_projects_3.setFrameShadow(QFrame.Shadow.Raised)
        self.table_projects_3.setShowGrid(True)
        self.table_projects_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_3.addWidget(self.main_3, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyLive Engine", None))
        self.header_3.setTitle("")
        self.logo_icon_3.setText("")
        self.logo_text_3.setText(QCoreApplication.translate("MainWindow", u"PyLive Engine", None))
        self.version_3.setText(QCoreApplication.translate("MainWindow", u"version dev", None))
        self.main_3.setTitle("")
        self.projects_3.setText(QCoreApplication.translate("MainWindow", u"Projects", None))
        self.project_choose_3.setTitle("")
        self.text_3.setText(QCoreApplication.translate("MainWindow", u"Projects", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"ADD", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"NEW", None))
    # retranslateUi