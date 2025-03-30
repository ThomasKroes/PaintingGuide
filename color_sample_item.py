import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer

from color_swatch_item import ColorSwatchItem

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class ColorSampleItem(QGraphicsEllipseItem):
    radius              = 40
    border_thickness    = 4
    border_color        = ColorSwatchItem.border_color_active

    def __init__(self, color_sample):
        super().__init__()
        
        self.color_sample           = color_sample
        self.anchor_position_scene  = QPointF()

        self.setPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), ColorSampleItem.border_thickness))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        self.color_sample.position_changed.connect(self.position_changed)
        self.color_sample.color_changed.connect(self.color_changed)

        self.set_position(self.color_sample.position)
        self.set_position(self.color_sample.position)

    def position_changed(self, position : QPointF):
        """Invoked when the color sample color changes."""
        
        self.set_position(position)

    def color_changed(self, color : QColor):
        """Invoked when the color sample color changes."""
        
        self.set_color(color)

    def set_position(self, center : QPointF):
        """Set the item center."""

        self.setRect(center.x() - ColorSampleItem.radius / 2, center.y() - ColorSampleItem.radius / 2, ColorSampleItem.radius, ColorSampleItem.radius)

    def set_color(self, color):
        """Set the item color."""

        self.setBrush(QBrush(color))

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemVisibleHasChanged or change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.color_sample.set_position(self.mapToScene(self.rect().center()))

        return super().itemChange(change, value)
   
   