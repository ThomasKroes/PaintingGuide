from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QObject, QLineF, pyqtSignal

from color_sample_link_item import ColorSampleLinkItem

class ColorSampleLink(QObject):
    color_sample_links      = list()
    occupied_color_swatches = list()
    visible_changed         = pyqtSignal(bool)
    active_changed          = pyqtSignal(bool)

    def __init__(self, color_sample, color_swatch):
        super().__init__()

        ColorSampleLink.color_sample_links.append(self)

        self.visible                = False
        self.active                 = False
        self.color_sample           = color_sample
        self.color_swatch           = color_swatch
        self.distance               = 0
        self.color_sample_link_item = ColorSampleLinkItem(self)

        self.color_sample.project.scene.addItem(self.color_sample_link_item)
        
        self.color_sample.anchor_changed.connect(self.update_line)
        self.color_swatch.anchor_changed.connect(self.update_line)
        
        self.update_line()

    def __del__(self):
        """Remove color sample link from tracking when deleted."""

        if self in ColorSampleLink.color_sample_links:
            ColorSampleLink.color_sample_links.remove(self)

    def update_distance(self):
        """Computes the distance between the color sample and the color swatch."""

        self.distance = (QVector2D(self.color_sample.anchor) - QVector2D(self.color_swatch.anchor)).length()

    def update_line(self):
        """Updates the line segment."""

        self.color_sample_link_item.set_line(QLineF(self.color_sample.anchor, self.color_swatch.anchor))

    def set_visible(self, visible : bool):
        """Set link visibility"""

        if visible is not self.visible:
            self.visible = visible

        self.visible_changed.emit(self.visible)

    def activate(self):
        """Activate the link."""

        if not self.active:
            self.active = True

            self.active_changed.emit(self.active)

            ColorSampleLink.occupied_color_swatches.append(self.color_swatch)

    def deactivate(self):
        """De-activate the link."""

        if self.active:
            self.active = False

            self.active_changed.emit(self.active)

            ColorSampleLink.occupied_color_swatches.remove(self.color_swatch)
