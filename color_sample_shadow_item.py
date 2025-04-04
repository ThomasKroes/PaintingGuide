from PyQt6.QtCore import Qt, QPointF

from graphics_widget import GraphicsWidget
from common import *
from styling import *

class ColorSampleShadowItem(GraphicsWidget):
    items = list()

    def __init__(self, color_sample):
        super().__init__()
        
        ColorSampleShadowItem.items.append(self)

        self.color_sample   = color_sample
        self.path           = None

        self.setGeometry(self.boundingRect())
        self.setZValue(2)

    def __del__(self):
        """Remove color sample shadow item from tracking when deleted."""

        self.print("Delete")

    def boundingRect(self):
        """Return the bounding rectangle for the item."""

        margin  = 10
        margins = QMarginsF(margin, margin, margin, margin)

        if not self.path:
            return QRectF(QPointF(), QSizeF(100, 100))

        return self.path.boundingRect()
    
    def paint(self, painter: QPainter, option, widget=None):
        if not self.path:
            return
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawPath(self.path)