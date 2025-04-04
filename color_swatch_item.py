from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QSizeF, QPointF
from PyQt6.QtWidgets import QGraphicsItem

from graphics_widget import GraphicsWidget
from drop_shadow_mixin import DropShadowMixin

from styling import *

from common import *

class ColorSwatchItem(GraphicsWidget, DropShadowMixin):
    swatch_size     = 250
    swatch_spacing  = swatch_size / 5
    margin          = 20
    items           = list()

    def __init__(self, color_swatch):
        GraphicsWidget.__init__(self)
        DropShadowMixin.__init__(self)

        ColorSwatchItem.items.append(self)
        
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsScenePositionChanges)
        self.setZValue(1)

        self.color_swatch           = color_swatch
        self.corner_radius          = ColorSwatchItem.swatch_size / 5
        self.border_width           = ColorSwatchItem.swatch_size / 25
        self.anchor_position_scene  = QPointF()

        self.size = QSizeF(ColorSwatchItem.swatch_size, ColorSwatchItem.swatch_size)

        self.setPreferredSize(self.size)
        self.setMinimumSize(self.size)
        self.setMaximumSize(self.size)
        self.setContentsMargins(0, 0, 0, 0)

        self.color_swatch.color_changed.connect(self.update)
        self.color_swatch.active_changed.connect(self.update)
        self.color_swatch.position_changed.connect(self.set_position)

    def set_position(self, position):

        self.setPos(position)

    def boundingRect(self) -> QRectF:
        width = self.size.width()
        height = self.size.height()

        return QRectF(-width / 2, -height / 2, width, height)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(self.color_swatch.color))
        painter.setPen(get_item_pen(self))
        painter.drawRoundedRect(self.boundingRect(), self.corner_radius, self.corner_radius)

