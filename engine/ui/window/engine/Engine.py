from PySide6.QtCore import (
    QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt
)
from PySide6.QtGui import (
    QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform
)
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLayout, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget
)
from PySide6.scripts.pyside_tool import project

import engine.ui.window.engine.Engine_rc
from engine.core.Project import Project
from engine.ui.lang.TextTranslater import text_translator
from engine.ui.widget.Engine.FileManagerWidget import FileManagerWidget
from engine.ui.widget.Engine.GameEditorWidget import GameEditorWidget
from engine.ui.widget.Engine.HierarchyWidget import HierarchyWidget
from engine.ui.widget.Engine.PropertyWidget import PropertyEditor
from engine.ui.window.engine.Engine_logic import Engine
from engine.ui.window.engine.settings.Settings import Settings_UI, SettingsDialog


class EngineUI:
    def __init__(self, main_window, project: Project):
        self.project = project
        self.project.set_notify_for_change_scene(notify=self.change_scene)
        self.engine = Engine(project)
        self.game_editor = None
        self.main_window = main_window
        self.setup_ui(main_window)
        self.project.settings.subscribe_change_title(self.update_title)

    def setup_ui(self, main_window):
        """Setup UI elements for the main window."""

        if not main_window.objectName():
            main_window.setObjectName(self.project.settings.name_project)
        main_window.resize(1200, 720)
        main_window.setMinimumSize(QSize(720, 520))
        main_window.setMaximumSize(QSize(16777215, 16777215))

        self.apply_modern_style()

        # Set window icon
        icon = QIcon()
        icon.addFile(u":/icon/snake.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        main_window.setWindowIcon(icon)

        # Setup actions
        self.setup_actions(main_window)

        # Central widget and layouts
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"centralwidget")
        self.horizontal_layout = QHBoxLayout(self.central_widget)
        self.horizontal_layout.setObjectName(u"horizontalLayout")

        # Initialize main sections
        self.initialize_sections()

        main_window.setCentralWidget(self.central_widget)

        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        main_window.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        # Setup menu
        self.setup_menu()

        self.retranslate_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

    def setup_actions(self, main_window):
        """Setup actions for the main window."""
        self.action_save = QAction(main_window)
        self.action_save.setObjectName(u"action_save")
        self.action_save.triggered.connect(self.save_project)

        self.action_exit = QAction(main_window)
        self.action_exit.setObjectName(u"action_exit")

        self.action_exit.triggered.connect(self.exit_app)

        self.action_settings = QAction(main_window)
        self.action_settings.setObjectName(u"action_settings")
        self.action_settings.triggered.connect(self.open_settings_window)
        self.action_about = QAction(main_window)
        self.action_about.setObjectName(u"action_about")

    def update_title(self):
        self.main_window.setWindowTitle(QCoreApplication.translate("MainWindow", self.project.settings.name_project, None))

    def exit_app(self):
        self.main_window.close()

    def save_project(self):
        for scene in self.project.get_scenes():
            scene.save()

    def open_settings_window(self):
        self.settings_dialog = SettingsDialog(self.project, self)
        self.settings_dialog.exec_()

    def change_scene(self):
        self.project.get_current_scene().load_objects()
        self.clear_layout(self.horizontal_layout)
        self.initialize_sections()

    def clear_layout(self, layout: QLayout):
        """Clear all widgets from the layout."""
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    self.clear_layout(child.layout())

    def initialize_sections(self):
        """Initialize main sections of the UI."""
        self.horizontal_layout_8 = QHBoxLayout()
        self.horizontal_layout_8.setObjectName(u"horizontalLayout_8")
        self.horizontal_layout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)

        # Hierarchy section
        self.hierarchy = QHBoxLayout()
        self.property_editor = PropertyEditor()
        self.hierarchy_widget = HierarchyWidget(self.engine.project.get_current_scene())
        self.hierarchy_widget.subscribe_by_update_object(self.property_editor.update_object)
        self.hierarchy_widget.subscribe_by_item_choose(self.property_editor.set_current_object)

        self.hierarchy.addWidget(self.hierarchy_widget)
        self.hierarchy.setObjectName(u"hierarchy")
        self.horizontal_layout_8.addLayout(self.hierarchy)

        # Main section
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName(u"main")
        self.game_layout = QVBoxLayout()
        if self.game_editor:
            self.game_editor.game.stop()
        self.game_editor = GameEditorWidget(self.project)
        self.game_layout.addWidget(self.game_editor)
        self.game_layout.setObjectName(u"game")

        self.main_layout.addLayout(self.game_layout)

        self.file_explorer_layout = QVBoxLayout()
        self.file_manager = FileManagerWidget(self.engine.project.path_project)
        self.file_explorer_layout.addWidget(self.file_manager)
        self.file_explorer_layout.setObjectName(u"file_explorer")

        self.main_layout.addLayout(self.file_explorer_layout)

        self.main_layout.setStretch(0, 3)
        self.main_layout.setStretch(1, 2)
        self.horizontal_layout_8.addLayout(self.main_layout)

        # Properties section
        self.properties_layout = QHBoxLayout()
        self.properties_layout.setObjectName(u"properties")
        self.properties_layout.addWidget(self.property_editor)

        self.horizontal_layout_8.addLayout(self.properties_layout)

        self.horizontal_layout_8.setStretch(0, 1)
        self.horizontal_layout_8.setStretch(1, 3)
        self.horizontal_layout_8.setStretch(2, 1)

        if self.horizontal_layout.itemAt(0):
            self.horizontal_layout.removeItem(self.horizontal_layout.itemAt(0))
        self.horizontal_layout.addLayout(self.horizontal_layout_8)

    def setup_menu(self):
        """Setup menu for the main window."""
        self.menu_project = QMenu(self.menubar)
        self.menu_project.setObjectName(u"menu_project")
        self.menu_about = QMenu(self.menubar)
        self.menu_about.setObjectName(u"menu_about")

        self.menubar.addAction(self.menu_project.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())
        self.menu_project.addAction(self.action_settings)
        self.menu_project.addAction(self.action_save)
        self.menu_project.addAction(self.action_exit)
        self.menu_about.addAction(self.action_about)

    def apply_modern_style(self):
        """Apply a modern style to the widget."""
        QApplication.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(palette)

    def retranslate_ui(self, main_window):
        """Set text translation for UI elements."""
        main_window.setWindowTitle(QCoreApplication.translate("MainWindow", self.project.settings.name_project, None))
        self.action_save.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.project.save"), None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.project.exit"), None))
        self.action_settings.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.project.settings"), None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.help.documentation"), None))
        self.menu_project.setTitle(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.project"), None))
        self.menu_about.setTitle(QCoreApplication.translate("MainWindow", text_translator.get_translate("window.menu_bar.help"), None))
