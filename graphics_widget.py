from PyQt6.QtWidgets import QLabel, QGraphicsWidget, QGraphicsItem, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF

from debug_print_mixin import DebugPrintMixin

class GraphicsWidget(QGraphicsWidget, DebugPrintMixin):
    def __init__(self):
        QGraphicsWidget.__init__(self)
        DebugPrintMixin.__init__(self)

        self.selected = False

    def set_fixed_size(self, size : QSizeF):
        """Set fixed size."""

        self.resize(size)
        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def set_selected(self, selected : bool):
        """Set selected."""

        if selected is self.selected:
            return
        
        self.selected = selected

        self.update()
   
    