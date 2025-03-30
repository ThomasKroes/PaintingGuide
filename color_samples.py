import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QMarginsF

from color_sample_item import ColorSampleItem

class ColorSamples(QObject):
    def __init__(self, project):
        super().__init__()

        self.project = project

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            color_samples = list()

            for color_sample_item in ColorSampleItem.items:
                color_samples.append(color_sample_item.to_dict())

            dict["ColorSamples"] = color_samples
        except Exception as e:
            print(f"Unable to save color samples to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            for color_sample_dict in dict["ColorSamples"]:
                ColorSampleItem.create_from_dict(self.project, color_sample_dict)

            for color_sample_item in ColorSampleItem.items:
                color_sample_item.update()
                
        except Exception as e:
            print(f"Unable to load color samples from dictionary: {e}")
            traceback.print_exc()