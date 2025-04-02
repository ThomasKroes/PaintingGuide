import traceback

from PyQt6.QtGui import QColor
from PyQt6.QtCore import QObject, QPointF, pyqtSignal

from color_sample_item import ColorSampleItem
from color_sample_link import ColorSampleLink
from color_swatch import ColorSwatch

from color_swatches import ColorSwatches

from common import *

class ColorSample(QObject):
    color_samples       = list()
    position_changed    = pyqtSignal(QPointF)
    anchor_changed      = pyqtSignal(QPointF)
    color_changed       = pyqtSignal(QColor)

    def __init__(self, project, position=QPointF()):
        super().__init__()

        ColorSample.color_samples.append(self)

        self.verbose                = True
        self.project                = project
        self.position               = QPointF(position)
        self.anchor                 = QPointF(position)
        self.color                  = QColor()
        self.color_sample_item      = ColorSampleItem(self)
        
        self.project.scene.addItem(self.color_sample_item)

        self.project.color_swatches.swatches_changed.connect(self.update_candidate_links)

        self.update_candidate_links()

    def __debug_print__(self, message : str):
        """Print a nicely formatted debug message."""

        if self.verbose:
            if self in ColorSample.color_samples:
                print(f"{ __class__.__name__ } { ColorSample.color_samples.index(self) + 1 }: { message }")
            else:
                print(f"{ __class__.__name__ }: { message }")

    def __del__(self):
        """Remove color sample from tracking when deleted."""

        self.__debug_print__("Delete")
    
    def remove(self):
        """Remove the color sample and the associated items."""
        
        self.__debug_print__("Remove")

        self.project.scene.removeItem(self.color_sample_item)

        if self in ColorSample.color_samples:
            ColorSample.color_samples.remove(self)

        for color_sample_link in ColorSampleLink.color_sample_links:
            if color_sample_link.color_sample is self:
                color_sample_link.remove()

        del self

    def update_candidate_links(self):
        """Creates all candidate links with the color swatches."""

        self.__debug_print__(f"Update candidate links")

        for color_swatch in ColorSwatch.color_swatches:
            ColorSampleLink(self, color_swatch)

    def set_position(self, position : QPointF):
        """Set position in scene coordinates."""

        self.__debug_print__(f"Set position: { qpointf_to_string(position) }")

        if position is not self.position:
            self.position = position

            self.position_changed.emit(self.position)

            reference_position = self.project.reference_item.mapFromScene(self.position)
            
            self.set_anchor(self.position)
            self.set_color(self.project.reference_image.pixelColor(reference_position.toPoint()))
            self.project.color_sample_links.choose_links()
            
    def set_anchor(self, anchor : QPointF):
        """Set anchor in scene coordinates."""

        self.__debug_print__(f"Set anchor: { qpointf_to_string(anchor) }")

        if anchor is not self.anchor:
            self.anchor = anchor
            
            self.anchor_changed.emit(self.anchor)

    def set_color(self, color : QColor):
        """Set color."""

        self.__debug_print__(f"Set color: { qcolor_to_rgb_string(color) }")

        if color is self.color:
            return
        
        self.color = color

        self.color_changed.emit(self.color)

    def save_to_dict(self):
        """Save in dictionary."""

        try:
            self.__debug_print__(f"Save to dict: { qpointf_to_string(self.position) }, { qcolor_to_rgb_string(self.color) }")

            color_sample_dict = dict()

            color_sample_dict["Position"]   = qpointf_to_dict(self.position)
            color_sample_dict["Color"]      = qcolor_to_dict(self.color)

            return color_sample_dict
        except Exception as e:
            print(f"Unable to save color sample to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            self.set_position(qpointf_from_dict(dict["Position"]))
            self.set_color(qcolor_from_dict(dict["Color"]))

            self.__debug_print__(f"Load from dict: { qpointf_to_string(self.position) }, { qcolor_to_rgb_string(self.color) }")

            # reference_position = self.project.reference_item.mapFromScene(self.position)

            # self.set_color(self.project.reference_image.pixelColor(reference_position.toPoint()))
            # self.project.color_sample_links.choose_links()

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