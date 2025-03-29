from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF

from graphics_widget import GraphicsWidget
from color_swatch_item import ColorSwatchItem

class ReferenceItem(GraphicsWidget):
    def __init__(self, project):
        super().__init__()
        
        self.setZValue(-100)

        self.project = project

    def paint(self, painter, option, widget=None):
        """Override the paint method for customization."""
        
        if self.project.reference_image:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.project.reference_image))

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(ColorSwatchItem.border_color_inactive)
        painter.drawRect(self.rect())
   
    