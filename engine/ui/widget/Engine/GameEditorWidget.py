import pygame
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage, Qt
from PySide6.QtCore import QTimer

from core.Core import Game
from engine.core.Project import Project


class GameEditorWidget(QWidget):
    def __init__(self, project: Project, parent=None):
        super().__init__(parent)
        self.project = project
        self.game = Game(project.settings)
        self.game.set_scene(project.get_current_scene())
        self.game.run(dev=True)
        self.initUI()
        self.start_rendering()

    def initUI(self):
        self.setWindowTitle("Game Editor")
        self.setGeometry(100, 100, 800, 600)

    def paintEvent(self, event):
        self.runRenderPygame()

    def hideEvent(self, event):
        self.game.stop()

    def runRenderPygame(self):
        painter = QPainter(self)
        render = self.game.get_render()
        if render:
            screen = render.get_surface()
            pygame_img = pygame.image.tostring(screen, "RGB")
            qimage = QImage(pygame_img, screen.get_width(), screen.get_height(), QImage.Format_RGB888)
            painter.drawImage(0, 0, qimage)

    def start_rendering(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // 30)  # 60 FPS

    def mousePressEvent(self, event):
        # Handle mouse clicks in pygame
        if event.button() == Qt.LeftButton:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(event.x(), event.y())))

    def keyPressEvent(self, event):
        # Handle key presses in pygame
        key = event.key()
        pygame_key = self.convertToPygameKey(key)
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame_key))

    def keyReleaseEvent(self, event):
        # Handle key releases in pygame
        key = event.key()
        pygame_key = self.convertToPygameKey(key)
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame_key))

    def convertToPygameKey(self, qt_key):
        # Replace this method to convert Qt key to pygame key
        return qt_key  # Placeholder, needs actual mapping implementation