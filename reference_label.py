from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QPoint

from color_sample_item import ColorSampleItem

class ReferenceLabel(QLabel):
    def __init__(self, project):
        super().__init__()
            
        self.project = project

    def pixel_color(self, coordinates : QPoint):
        """Get pixel color from coordinates."""

        return self.project.reference_image.pixelColor(coordinates)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.project.reference_image:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.project.reference_image))

        #     painter.setPen(QPen(ColorSample.border_color, ColorSample.border_thickness))
            
        #     for color_sample in self.project.color_samples:
        #         painter.setBrush(QBrush(color_sample.color))
        #         painter.drawEllipse(color_sample.position, ColorSample.radius, ColorSample.radius)
        
        super().paintEvent(event)

