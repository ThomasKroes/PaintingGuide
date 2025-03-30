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

    #     def connect_to_color_swatch_item(self, color_swatch_item):
    #     """Connect to color swatch item."""

    #     print(__name__, color_swatch_item)

    #     self.color_swatch_item = color_swatch_item

    #     self.color_swatch_item.connect_to_color_sample_item(self)

    #     self.color_swatch_item.sample_color = self.brush().color()

        
    #     line = QLineF(self.anchor_position_scene, self.color_swatch_item.anchor_position_scene)

    #     if line is not self.link_item.line():
    #         # self.link_item.fade_out()
    #         self.link_item.setLine(line)
    #         # self.link_item.fade_in()

    # def disconnect_from_color_swatch_item(self):
    #     """Disconnect from color swatch item."""

    #     self.color_swatch_item = None