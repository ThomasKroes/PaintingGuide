from PyQt6.QtGui import QPainter, QBrush, QPainterPath
from PyQt6.QtCore import QRectF, QPointF

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
        self.anchor_position_scene  = QPointF()

        self.color_swatch.color_changed.connect(self.update)
        self.color_swatch.active_changed.connect(self.update)
        self.color_swatch.position_changed.connect(self.set_position)

    def set_position(self, position):

        self.setPos(position)

    def boundingRect(self) -> QRectF:
        """Get the bounding rectangle."""

        return self.shape().boundingRect()
    
    def shape(self):
        """Get shape for more accurate selection."""

        path        = QPainterPath()
        size        = ColorSwatchItem.swatch_size
        half_size   = size / 2

        path.addRoundedRect(QRectF(-half_size, -half_size, size, size), self.corner_radius, self.corner_radius)

        return path

    def paint(self, painter: QPainter, option, widget=None):
        """Override to draw custom color swatch."""

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(self.color_swatch.color))
        painter.setPen(get_item_pen(self))
        painter.drawPath(self.shape())


