from datetime import datetime
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt, QAbstractTableModel)
from PySide6.QtGui import (QCursor, QFont, QIcon, QPixmap)
from PySide6.QtWidgets import (QFrame, QGridLayout, QGroupBox, QHeaderView, QLabel, QPushButton,
                               QScrollArea, QSizePolicy, QTableView, QWidget, QStyledItemDelegate,
                               QDialog, QLineEdit, QFileDialog, QMessageBox, QVBoxLayout, QComboBox)

from core.Constants import VERSION_ENGINE
from engine.core.Loader import Loader
from engine.ui.lang.TextTranslater import text_translator, languages
from engine.ui.window.project_manager.ProjectManager_logic import LastProject, Projects


class ProjectViewer(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.items = []

    def setItems(self, items):
        self.beginResetModel()
        self.items = items
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self.items)

    def columnCount(self, parent=None):
        return 3

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        project = self.items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return project['name']  # Project name
            elif index.column() == 1:
                return project['version']  # Project version
            elif index.column() == 2:
                return project['last_open']  # Last opened date

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            header_labels = {
                0: text_translator.get_translate("window.project_manager.projects.table.project_name"),
                1: text_translator.get_translate("window.project_manager.projects.table.engine_version"),
                2: text_translator.get_translate("window.project_manager.projects.table.last_open")
            }
            return header_labels.get(section)
        return None


class ProjectDialog(QDialog):
    def __init__(self, loader: Loader, projects: Projects):
        super().__init__()
        self.loader = loader
        self.projects = projects
        self.setWindowTitle("Создание нового проекта")

        # Field for project name input
        self.name_label = QLabel("Название проекта:")
        self.name_input = QLineEdit()

        # Field for project path
        self.path_label = QLabel("Путь до папки проекта:")
        self.path_input = QLineEdit()
        self.path_button = QPushButton("Выбрать путь")
        self.path_button.clicked.connect(self.select_path)

        # Button to create project
        self.create_button = QPushButton("Создать")
        self.create_button.clicked.connect(self.create_project)

        # Vertical layout for placing widgets
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.path_button)
        layout.addWidget(self.create_button)
        self.setLayout(layout)

    def select_path(self):
        # Open directory dialog
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для проекта")
        if folder_path:
            self.path_input.setText(folder_path)

    def create_project(self):
        # Get project name and path
        project_name = self.name_input.text()
        project_path = self.path_input.text()

        # Validate fields
        if not project_name or not project_path:
            QMessageBox.warning(self, "Ошибка", "Введите название и путь до папки проекта")
            return

        # Create and add new project
        project = self.loader.create_project(project_path, project_name)
        self.projects.add_new_project(
            LastProject(project.settings.name_project, project_path, project.settings.version_engine,
                        datetime.today().date().isoformat()))
        self.accept()


class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, func, model, projects: Projects, parent=None):
        super().__init__(parent)
        self.func = func
        self.model = model
        self.projects = projects

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseButtonRelease:
            # Update the last_open date and save the project
            self.projects.get_last_projects()[index.row()].last_open = datetime.today().date().isoformat()
            self.projects.save()
            self.func(self.model.items[index.row()]["path"])
            return True
        return super().editorEvent(event, model, option, index)


class ProjectManager_UI:
    def __init__(self, MainWindow):
        self.setupUi(MainWindow)
        self.projects = Projects()
        self.loader = Loader(MainWindow)
        self.MainWindow = MainWindow
        self.model = ProjectViewer()
        self.model.setItems(self.projects.get_formatted_last_projects())
        self.table_projects_3.setModel(self.model)

        # Setup table properties
        self.setup_table_properties()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 560)
        MainWindow.setMinimumSize(QSize(900, 560))
        MainWindow.setMaximumSize(QSize(900, 560))

        # Set MainWindow icon
        icon = QIcon()
        icon.addFile(":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 901, 561))
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(25)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)

        self.setup_header()
        self.setup_main_section()
        self.all_menus = []
        self.setup_project_selection_section()
        self.setup_settings_section()  # Настройки
        self.setup_about_section()  # О нас

        MainWindow.setCentralWidget(self.centralwidget)

        # Retranslation and translation of UI elements
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def setup_header(self):
        self.header_3 = QGroupBox(self.layoutWidget)
        self.header_3.setObjectName("header_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_3.sizePolicy().hasHeightForWidth())
        self.header_3.setSizePolicy(sizePolicy)
        self.header_3.setMinimumSize(QSize(0, 50))
        self.header_3.setStyleSheet("background-color: #fff;\nborder: none;")

        self.logo_icon_3 = QLabel(self.header_3)
        self.logo_icon_3.setObjectName("logo_icon_3")
        self.logo_icon_3.setGeometry(QRect(10, 5, 40, 40))
        self.logo_icon_3.setMinimumSize(QSize(0, 40))
        self.logo_icon_3.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.logo_icon_3.setPixmap(QPixmap(":/icon/snake.png"))
        self.logo_icon_3.setScaledContents(True)

        self.logo_text_3 = QLabel(self.header_3)
        self.logo_text_3.setObjectName("logo_text_3")
        self.logo_text_3.setGeometry(QRect(60, 0, 101, 50))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logo_text_3.sizePolicy().hasHeightForWidth())
        self.logo_text_3.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setFamilies(["Microsoft JhengHei Light"])
        font.setPointSize(12)
        self.logo_text_3.setFont(font)
        self.logo_text_3.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.version_3 = QLabel(self.header_3)
        self.version_3.setObjectName("version_3")
        self.version_3.setGeometry(QRect(800, 0, 91, 50))
        sizePolicy1.setHeightForWidth(self.version_3.sizePolicy().hasHeightForWidth())
        self.version_3.setSizePolicy(sizePolicy1)
        self.version_3.setFont(font)
        self.version_3.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.version_3.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_3.addWidget(self.header_3, 0, 0, 1, 1)

    def setup_main_section(self):
        self.main_3 = QGroupBox(self.layoutWidget)
        self.main_3.setObjectName("main_3")
        self.main_3.setStyleSheet("border: none;")

        # Buttons section
        self.buttons_3 = QScrollArea(self.main_3)
        self.buttons_3.setObjectName("buttons_3")
        self.buttons_3.setGeometry(QRect(0, -11, 211, 491))
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttons_3.sizePolicy().hasHeightForWidth())
        self.buttons_3.setSizePolicy(sizePolicy2)
        self.buttons_3.setStyleSheet("border: none;")
        self.buttons_3.setWidgetResizable(True)

        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 211, 491))

        self.setup_buttons()

        self.buttons_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_3.addWidget(self.main_3, 1, 0, 1, 1)

    def setup_buttons(self):
        self.active_stylesheet_button = ("QPushButton {background-color: transparent;border: none;font-size: 14px;text-align: left;padding-left: 15px;border-left: 3px solid blue;}"
            "QPushButton:hover {background-color:white;cursor: pointer;}")

        self.stylesheet_button = (
            "QPushButton {background-color: transparent;border: none;font-size: 14px;text-align: left;padding-left: 15px;border-left: 3px solid transparent;}"
            "QPushButton:hover {background-color:white;cursor: pointer;}")

        self.projects_3 = QPushButton(self.scrollAreaWidgetContents_3)
        self.projects_3.setObjectName("projects_3")
        self.projects_3.setGeometry(QRect(0, 10, 211, 30))
        self.projects_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.projects_3.setStyleSheet(self.active_stylesheet_button)

        # Добавление кнопки "Настройки"
        self.settings_3 = QPushButton(self.scrollAreaWidgetContents_3)
        self.settings_3.setObjectName("settings_3")
        self.settings_3.setGeometry(QRect(0, 50, 211, 30))
        self.settings_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_3.setStyleSheet(self.stylesheet_button)

        # Добавление кнопки "О нас"
        self.about_3 = QPushButton(self.scrollAreaWidgetContents_3)
        self.about_3.setObjectName("about_3")
        self.about_3.setGeometry(QRect(0, 90, 211, 30))
        self.about_3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.about_3.setStyleSheet(self.stylesheet_button)

        # Обработчики нажатий на кнопки
        self.projects_3.clicked.connect(self.show_projects)
        self.settings_3.clicked.connect(self.show_settings)
        self.about_3.clicked.connect(self.show_about)

        self.all_buttons = [self.projects_3, self.settings_3, self.about_3]

    def setup_project_selection_section(self):
        self.project_choose_3 = QGroupBox(self.main_3)
        self.project_choose_3.setObjectName("project_choose_3")
        self.project_choose_3.setGeometry(QRect(220, 0, 671, 471))
        self.project_choose_3.setStyleSheet("border: none;")

        self.text_3 = QLabel(self.project_choose_3)
        self.text_3.setObjectName("text_3")
        self.text_3.setGeometry(QRect(10, 10, 81, 24))
        font1 = QFont()
        font1.setFamilies(["Trebuchet MS"])
        font1.setPointSize(16)
        self.text_3.setFont(font1)

        font2 = QFont()
        font2.setFamilies(["Verdana"])

        self.pushButton_5 = QPushButton(self.project_choose_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setGeometry(QRect(464, 10, 91, 24))
        self.pushButton_5.setFont(font2)
        self.pushButton_5.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_5.setStyleSheet("QPushButton {background-color: white;border: none;}"
                                        "QPushButton:hover {background-color: #cccccc;}")
        self.pushButton_5.clicked.connect(self.open_project)

        self.pushButton_6 = QPushButton(self.project_choose_3)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setGeometry(QRect(570, 10, 91, 24))
        self.pushButton_6.setFont(font2)
        self.pushButton_6.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_6.setStyleSheet("QPushButton {background-color: #55aaff;border: none;color: #fff;}"
                                        "QPushButton:hover {background-color: #4387ca;}")
        self.pushButton_6.clicked.connect(self.create_project_dialog)

        self.table_projects_3 = QTableView(self.project_choose_3)
        self.table_projects_3.setObjectName("table_projects_3")
        self.table_projects_3.setGeometry(QRect(10, 40, 651, 421))
        self.table_projects_3.setFrameShape(QFrame.Shape.Box)
        self.table_projects_3.setFrameShadow(QFrame.Shadow.Raised)
        self.table_projects_3.setShowGrid(True)
        self.table_projects_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.all_menus.append(self.project_choose_3)

    def setup_settings_section(self):
        self.settings_section = QGroupBox(self.main_3)
        self.settings_section.setObjectName("settings_section")
        self.settings_section.setGeometry(QRect(220, 0, 671, 471))
        self.settings_section.setStyleSheet("border: none;")
        self.settings_title = QLabel(self.settings_section)
        self.settings_title.setObjectName("settings_title")
        self.settings_title.setGeometry(QRect(10, 10, 120, 24))
        font1 = QFont()
        font1.setFamilies(["Trebuchet MS"])
        font1.setPointSize(16)
        self.settings_title.setFont(font1)
        self.language_label = QLabel(self.settings_section)
        self.language_label.setObjectName("language_label")
        self.language_label.setGeometry(QRect(10, 60, 300, 30))
        font2 = QFont()
        font2.setFamilies(["Verdana"])
        font2.setPointSize(10)
        self.language_label.setFont(font2)
        # Dropdown для выбора языка (реализуйте функцию выбора языка)
        self.language_dropdown = QComboBox(self.settings_section)
        self.language_dropdown.setObjectName("language_dropdown")
        self.language_dropdown.setGeometry(QRect(10, 100, 150, 20))
        self.language_dropdown.setFont(font2)
        self.load_languages()
        self.settings_section.hide()

        self.all_menus.append(self.settings_section)

    def change_language(self):
        current_language = self.language_dropdown.currentText()
        text_translator.switch_language(languages[current_language])
        self.retranslateUi(self.MainWindow)

    def load_languages(self):
        languages = self.get_available_languages()
        self.language_dropdown.addItems(languages)
        self.language_dropdown.currentIndexChanged.connect(self.change_language)

    def get_available_languages(self):
        languages = text_translator.get_languages()
        # Здесь должна быть реализация получения списка языков, например:
        return languages

    def setup_about_section(self):
        self.about_section = QGroupBox(self.main_3)
        self.about_section.setObjectName("about_section")
        self.about_section.setGeometry(QRect(220, 0, 671, 471))
        self.about_section.setStyleSheet("border: none;")
        self.about_title = QLabel(self.about_section)
        self.about_title.setObjectName("about_title")
        self.about_title.setGeometry(QRect(10, 10, 81, 24))
        font1 = QFont()
        font1.setFamilies(["Trebuchet MS"])
        font1.setPointSize(16)
        self.about_title.setFont(font1)
        self.about_text = QLabel(self.about_section)
        self.about_text.setObjectName("about_text")
        self.about_text.setGeometry(QRect(10, 20, 600, 200))
        self.about_text.setWordWrap(True)
        font2 = QFont()
        font2.setFamilies(["Verdana"])
        font2.setPointSize(10)
        self.about_text.setFont(font2)
        self.about_section.hide()

        self.all_menus.append(self.about_section)

    def setup_table_properties(self):
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

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "PyLive Engine", None))
        self.header_3.setTitle("")
        self.logo_icon_3.setText("")
        self.logo_text_3.setText(QCoreApplication.translate("MainWindow", "PyLive Engine", None))
        self.version_3.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.version") + f" {VERSION_ENGINE}", None))
        self.main_3.setTitle("")
        self.projects_3.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.button.projects"), None))
        self.settings_3.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.button.settings"), None))
        self.about_3.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.button.about"), None))
        self.project_choose_3.setTitle("")
        self.text_3.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.projects.title"), None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.projects.button.add"), None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate(
            "window.project_manager.projects.button.new"), None))
        self.settings_title.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.project_manager.settings.title"), None))
        self.language_label.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.project_manager.settings.choose_language"), None))
        self.about_title.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.project_manager.about_us.title"), None))
        self.about_text.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.project_manager.about_us_text"), None))

    def show_projects(self):
        for menu in self.all_menus:
            menu.hide()
        self.project_choose_3.show()
        for button in self.all_buttons:
            button.setStyleSheet(self.stylesheet_button)
        self.projects_3.setStyleSheet(self.active_stylesheet_button)

    def show_settings(self):
        for menu in self.all_menus:
            menu.hide()
        self.settings_section.show()
        for button in self.all_buttons:
            button.setStyleSheet(self.stylesheet_button)
        self.settings_3.setStyleSheet(self.active_stylesheet_button)

    def show_about(self):
        for menu in self.all_menus:
            menu.hide()
        self.about_section.show()
        for button in self.all_buttons:
            button.setStyleSheet(self.stylesheet_button)
        self.about_3.setStyleSheet(self.active_stylesheet_button)
