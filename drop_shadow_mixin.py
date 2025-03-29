from PyQt6.QtWidgets import QLabel, QGraphicsWidget, QGraphicsItem, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF

class DropShadowMixin():
    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(7)
        shadow.setOffset(7, 7)
        shadow.setColor(QColor(0, 0, 0, 100))

        self.setGraphicsEffect(shadow)