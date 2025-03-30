from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QObject

class ColorSampleLinks(QObject):
    links = list()

    def __init__(self, project):
        super().__init__()

        self.project = project
