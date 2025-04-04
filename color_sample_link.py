from PyQt6.QtGui import QVector2D, QColor
from PyQt6.QtCore import QObject, QLineF, pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsEllipseItem

from debug_print_mixin import DebugPrintMixin
from color_sample_link_item import ColorSampleLinkItem
from common import *

class ColorSampleLink(QObject, DebugPrintMixin):
    color_sample_links      = list()
    occupied_color_swatches = list()
    visible_changed         = pyqtSignal(bool)
    active_changed          = pyqtSignal(bool)

    def __init__(self, color_sample, color_swatch):
        QObject.__init__(self)
        DebugPrintMixin.__init__(self)

        ColorSampleLink.color_sample_links.append(self)

        self.set_print_index(ColorSampleLink.color_sample_links.index(self) + 1)

        self.visible                = False
        self.active                 = False
        self.color_sample           = color_sample
        self.color_swatch           = color_swatch
        self.distance               = 0
        self.color_sample_link_item = ColorSampleLinkItem(self)
        self.verbose                = True

        self.color_sample.project.scene.addItem(self.color_sample_link_item)
        
        self.color_sample.anchor_changed.connect(self.update_line)
        self.color_swatch.anchor_changed.connect(self.update_line)
        self.color_sample.color_changed.connect(self.update_color_swatch_color)
        self.color_sample.selected_changed.connect(self.color_sample_selected_changed)

        self.update_line()
    
    def __del__(self):
        """Remove color sample link from tracking when deleted."""

        self.print("Delete")

        # self.color_sample.project.scene.removeItem(self.color_sample_link_item)

    def remove(self):
        """Remove the color sample link and the associated items."""

        self.print("Remove")

        self.color_sample_link_item.remove()

        self.color_sample.anchor_changed.disconnect(self.update_line)
        self.color_swatch.anchor_changed.disconnect(self.update_line)
        self.color_sample.color_changed.disconnect(self.update_color_swatch_color)
        
        self.color_swatch.deactivate()
        
        del self.color_sample_link_item
        del self

    def color_sample_selected_changed(self, selected : bool):
        """Invoked when the color sample is selected or de-selected."""

        self.color_sample_link_item.set_selected(selected)
        
        # if self.active:
        #     self.color_swatch.color_swatch_item.set_selected(selected)

    def update_distance(self):
        """Computes the distance between the color sample and the color swatch."""

        self.distance = (QVector2D(self.color_sample.anchor) - QVector2D(self.color_swatch.anchor)).length()

    def update_line(self):
        """Updates the line segment."""

        self.color_sample_link_item.set_line(QLineF(self.color_sample.anchor, self.color_swatch.anchor))

        self.update_distance()

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

            self.color_swatch.set_color(self.color_sample.color)
            self.color_swatch.activate(self)
            self.color_sample.activate(self)
            
            # self.color_swatch.color_swatch_item.set_selected(self.color_sample.selected)

    def deactivate(self):
        """De-activate the link."""

        if self.active:
            self.active = False

            self.active_changed.emit(self.active)

            ColorSampleLink.occupied_color_swatches.remove(self.color_swatch)
            
            self.color_swatch.deactivate()
    
    def update_color_swatch_color(self, color : QColor):
        """Updates the color of the color swatch."""

        if self.active:
            self.color_swatch.set_color(color)