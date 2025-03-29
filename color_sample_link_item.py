import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer, QPropertyAnimation

class ColorSampleLinkItem(QGraphicsLineItem):
    items = list()

    def __init__(self, color_sample_item):
        super().__init__(parent=color_sample_item)

        ColorSampleLinkItem.items.append(self)

        self.setPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 4))

        # self.effect = QGraphicsOpacityEffect()

        # self.setGraphicsEffect(self.effect)
        
        # self.fade_animation = QPropertyAnimation(self.effect, b"opacity")
        
        # self.fade_animation.setDuration(500)

    def fade_in(self):
        """Fade in."""
        
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.start()

    def fade_out(self):
        """Fade out."""
        
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.start()

    def __del__(self):
        """Remove item from tracking when deleted."""

        if self in ColorSampleLinkItem.items:
            ColorSampleLinkItem.items.remove(self)
