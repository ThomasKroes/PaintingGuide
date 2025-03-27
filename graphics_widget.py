from PyQt6.QtWidgets import QLabel, QGraphicsWidget, QGraphicsItem
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF

class GraphicsWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()

    def set_fixed_size(self, size : QSizeF):
        """Set fixed size."""

        self.resize(size)
        self.setMinimumSize(size)
        self.setMaximumSize(size)

    
    