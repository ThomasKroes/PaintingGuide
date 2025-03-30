import traceback

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QObject, QPointF, pyqtSignal

from color_sample_item import ColorSampleItem
from color_sample_link_item import ColorSampleLinkItem

from common import *

class ColorSample(QObject):
    color_samples       = list()
    position_changed    = pyqtSignal(QPointF)
    color_changed       = pyqtSignal(QColor)

    def __init__(self, project, position=QPoint()):
        super().__init__()

        ColorSample.color_samples.append(self)

        self.project                = project
        self.position               = position
        self.color                  = QColor()
        self.color_sample_item      = ColorSampleItem(self)
        self.color_sample_link_item = ColorSampleLinkItem(self)

        self.project.scene.addItem(self.color_sample_item)
        self.project.scene.addItem(self.color_sample_link_item)

    def __del__(self):
        """Remove color sample from tracking when deleted."""

        if self in ColorSample.color_samples:
            ColorSample.color_samples.remove(self)

    def set_position(self, position : QPointF):
        """Set position in scene coordinates."""

        if position is self.position:
            return
        
        self.position = position

        self.position_changed.emit(self.position)

        reference_position = self.project.reference_item.mapFromScene(self.position)
        
        self.set_color(self.project.reference_image.pixelColor(reference_position.toPoint()))

    def set_color(self, color : QColor):
        """Set color."""

        if color is self.color:
            return
        
        self.color = color

        self.color_changed.emit(self.color)

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            dict["ColorSample"] = {
                "Position": qpointf_to_dict(self.position),
                "Color": qcolor_to_dict(self.color)
            }
        except Exception as e:
            print(f"Unable to save color sample to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            self.position   = qpointf_from_dict(dict["Position"])
            self.color      = qcolor_from_dict(dict["Color"])

            for color_sample_item in ColorSampleItem.items:
                color_sample_item.update()

            self.connect_all_samples()
        except Exception as e:
            print(f"Unable to load color sample from dictionary: {e}")
            traceback.print_exc()

    @staticmethod
    def create_from_dict(project, dict : dict):
        """Create a color sample from dictionary."""

        try:
            color_sample = ColorSample(project)

            color_sample.load_from_dict(dict)
        except Exception as e:
            print(f"Cannot create color sample item from dictionary: {e}")
            traceback.print_exc()

    @staticmethod
    def create_from_scene_position(project, scene_position : QPointF):
        """Create a color sample from scene position."""

        try:
            ColorSample(project, scene_position)
        except Exception as e:
            print(f"Cannot create color sample item from scene position: {e}")
            traceback.print_exc()