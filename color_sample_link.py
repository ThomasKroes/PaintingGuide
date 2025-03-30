from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QObject, QLineF

from color_sample_link_item import ColorSampleLinkItem

class ColorSampleLink(QObject):
    color_sample_links = list()

    def __init__(self, color_sample, color_swatch):
        super().__init__()

        ColorSampleLink.color_sample_links.append(self)

        self.color_sample           = color_sample
        self.color_swatch           = color_swatch
        self.color_sample_anchor    = QVector2D(self.color_sample.anchor)
        self.color_swatch_anchor    = QVector2D(self.color_swatch.anchor)
        self.distance               = (self.color_sample_anchor - self.color_swatch_anchor).length()
        self.color_sample_link_item = ColorSampleLinkItem(self)

        self.color_sample.project.scene.addItem(self.color_sample_link_item)
        
        self.color_sample.anchor_changed.connect(self.update_line)
        self.color_swatch.anchor_changed.connect(self.update_line)

        self.update_line()

    def __del__(self):
        """Remove color sample link from tracking when deleted."""

        if self in ColorSampleLink.color_sample_links:
            ColorSampleLink.color_sample_links.remove(self)

    def update_line(self):
        """Updates the line segment."""

        self.color_sample_link_item.setLine(QLineF(self.color_sample.anchor, self.color_swatch.anchor))
