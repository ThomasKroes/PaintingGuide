import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, pyqtSignal

from color_sample import ColorSample
from color_sample_item import ColorSampleItem
from color_swatch_item import ColorSwatchItem
from color_sample_link import ColorSampleLink

class ColorSamples(QObject):
    links                       = list()

    def __init__(self, project):
        super().__init__()

        self.project = project

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            color_samples = list()

            for color_sample in ColorSample.color_samples:
                color_samples.append(color_sample.save_to_dict())

            dict["ColorSamples"] = color_samples
        except Exception as e:
            print(f"Unable to save color samples to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            for color_sample_dict in dict["ColorSamples"]:
                ColorSample.create_from_dict(self.project, color_sample_dict)

        except Exception as e:
            print(f"Unable to load color samples from dictionary: {e}")
            traceback.print_exc()