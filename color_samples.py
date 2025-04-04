import traceback

from PyQt6.QtCore import QObject

from debug_print_mixin import DebugPrintMixin
from color_sample import ColorSample

class ColorSamples(QObject, DebugPrintMixin):
    def __init__(self, project):
        QObject.__init__(self)
        DebugPrintMixin.__init__(self)

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