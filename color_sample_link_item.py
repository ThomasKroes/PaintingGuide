import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer, QPropertyAnimation, QVariantAnimation

from graphics_widget import GraphicsWidget

class ColorSampleLinkItem(QGraphicsLineItem):
    def __init__(self, color_sample):
        super().__init__()

        self.color_sample   = color_sample
        self.line           = QLineF()

        self.color_sample.visible_changed.connect(self.update_visibility)

        self.animation = QVariantAnimation()

        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

        self.animation.setDuration(300)

        self.animation.valueChanged.connect(self.animate)
        
        self.setOpacity(0)
        self.setPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 4))

    def animate(self, value):
        self.setOpacity(value)
    
    def set_line(self, line):
        """Set link line segment."""

        self.line = line

        self.setLine(self.line)

    def update_visibility(self):
        """Update the visibility of the link."""

        if self.color_sample.visible:
            self.setOpacity(1)#self.fade_in()
        else:
            self.setOpacity(0)#self.fade_out()

    def fade_in(self):
        """Animate fade in."""
        
        self.animation.setDirection(QPropertyAnimation.Direction.Forward)
        self.animation.start()

    def fade_out(self):
        """Animate fade out."""

        self.animation.setDirection(QPropertyAnimation.Direction.Backward)
        self.animation.start()

        