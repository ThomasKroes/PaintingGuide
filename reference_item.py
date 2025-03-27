from PyQt6.QtGui import QPixmap

from graphics_widget import GraphicsWidget
from color_swatch import ColorSwatch

class ReferenceItem(GraphicsWidget):
    def __init__(self, project):
        super().__init__()
        
        self.project = project

    def paint(self, painter, option, widget=None):
        """Override the paint method for customization."""
        
        if self.project.reference_image:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.project.reference_image))

        painter.setPen(ColorSwatch.border_color_inactive)
        painter.drawRect(self.rect())
    
    