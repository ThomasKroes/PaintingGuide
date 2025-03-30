import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QMarginsF

from color_sample_item import ColorSampleItem
from color_swatch_item import ColorSwatchItem
from color_sample_link import ColorSampleLink

class ColorSamples(QObject):
    links = list()

    def __init__(self, project):
        super().__init__()

        self.project = project

    def connect_all_samples(self):
        """Connect all color samples to a color swatch."""

        print(__name__)

        try:
            ColorSamples.links = list()

            for color_sample_item in ColorSampleItem.items:
                color_sample_links = list()

                for color_swatch_item in [item for item in ColorSwatchItem.items if not item.color_sample_item]:
                    color_sample_links.append(ColorSampleLink(color_sample_item, color_swatch_item))

                if not color_sample_links:
                    continue

                color_sample_links.sort(key=lambda item: item.distance)

                color_sample_link = color_sample_links[0]
                color_sample_link.connect()
                
                ColorSamples.links.append(color_sample_link)
                
        except Exception as e:
            print(f"Unable to save connect all samples: {e}")
            traceback.print_exc()
        
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

            self.connect_all_samples()
        except Exception as e:
            print(f"Unable to load color samples from dictionary: {e}")
            traceback.print_exc()