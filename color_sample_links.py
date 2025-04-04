import traceback

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QApplication

from debug_print_mixin import DebugPrintMixin
from color_sample import ColorSample
from color_sample_link import ColorSampleLink

class ColorSampleLinks(QObject, DebugPrintMixin):
    def __init__(self, project):
        QObject.__init__(self)
        DebugPrintMixin.__init__(self)

        self.project = project

    def choose_links(self, force=False):
        """Choose best links from the list of candidate links."""

        if QApplication.instance().opening_project and not force:
            return
        
        # self.print("Choose links...")

        for link in ColorSampleLink.color_sample_links:
            link.deactivate()
            link.update_distance()

        for color_sample in ColorSample.color_samples:
            inactive_links  = [link for link in ColorSampleLink.color_sample_links if not link.color_swatch in ColorSampleLink.occupied_color_swatches]
            links           = [link for link in inactive_links if link.color_sample is color_sample]

            links.sort(key=lambda item: item.distance)
            
            distances = list()

            for l in links:
                distances.append(f"{ '{:.1f}'.format(l.distance)}")
            
            # print(distances, len(links))

            if links:
                links[0].activate()

        for link in ColorSampleLink.color_sample_links:
            link.set_visible(link.active)

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            pass
        except Exception as e:
            print(f"Unable to save color samples links to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            pass
        except Exception as e:
            print(f"Unable to load color sample links from dictionary: {e}")
            traceback.print_exc()
