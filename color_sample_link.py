from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QObject

class ColorSampleLink(QObject):
    def __init__(self, color_sample_item, color_swatch_item):
        super().__init__()

        self.color_sample_item      = color_sample_item
        self.color_swatch_item      = color_swatch_item
        self.color_sample_center    = QVector2D(self.color_sample_item.anchor_position_scene)
        self.color_swatch_center    = QVector2D(self.color_swatch_item.anchor_position_scene)
        self.distance               = (self.color_sample_center - self.color_swatch_center).length()

    def connect(self):
        """"""