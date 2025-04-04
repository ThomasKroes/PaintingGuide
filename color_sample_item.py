import traceback

from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneContextMenuEvent, QGraphicsWidget
from PyQt6.QtGui import QBrush, QVector2D
from PyQt6.QtCore import Qt, QPointF

from graphics_widget import GraphicsWidget
from drop_shadow_mixin import DropShadowMixin
from color_sample_context_menu import ColorSampleContextMenu
from color_swatch_item import ColorSwatchItem
from common import *
from styling import *

class ColorSampleItem(GraphicsWidget, DropShadowMixin):
    radius  = 50
    items   = list()

    def __init__(self, color_sample):
        GraphicsWidget.__init__(self)
        DropShadowMixin.__init__(self)
        
        ColorSampleItem.items.append(self)

        self.color_sample           = color_sample
        self.anchor_position_scene  = QPointF()
        self.verbose                = True
        self.initialized            = False
        
        self.setGeometry(self.boundingRect())
        self.setPos(self.color_sample.position)
        self.setZValue(4)

        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsScenePositionChanges)
        
        self.color_sample.position_changed.connect(self.position_changed)
        self.color_sample.color_changed.connect(self.update)
        
        self.update()
        
        self.initialized = True

    def __del__(self):
        """Remove color sample item from tracking when deleted."""

        self.print("Delete")

    def position_changed(self):
        """Invoked when the color sample position has changed."""

        self.setPos(self.color_sample.position)

    def itemChange(self, change, value):
        if not self.initialized:
            return super().itemChange(change, value)
        
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.color_sample.set_position(self.scenePos())

        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemSelectedHasChanged:
            self.color_sample.set_selected(self.isSelected())
            
        return super().itemChange(change, value)
    
    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        """Display a context menu at the cursor position."""

        color_sample_context_menu = ColorSampleContextMenu(self.color_sample)

        color_sample_context_menu.exec(event.screenPos())

    def boundingRect(self):
        """Return the bounding rectangle for the item."""

        return self.shape().boundingRect()
    
    def shape(self):
        path = QPainterPath()
        
        path.addEllipse(QPointF(), ColorSampleItem.radius, ColorSampleItem.radius)

        color_sample_link = self.color_sample.color_sample_link

        if color_sample_link:
            sample_anchor   = self.mapFromScene(color_sample_link.color_sample.anchor)
            swatch_anchor   = self.mapFromScene(color_sample_link.color_swatch.anchor)
            swatch_position = self.mapFromScene(color_sample_link.color_swatch.position)
            v_norm          = QVector2D(swatch_anchor - sample_anchor).normalized()

            path.moveTo(sample_anchor + (ColorSampleItem.radius * v_norm.toPointF()))
            path.lineTo(swatch_anchor)

            swatch_scene_size       = QSizeF(ColorSwatchItem.swatch_size, ColorSwatchItem.swatch_size)
            half_swatch_scene_size  = QSizeF(ColorSwatchItem.swatch_size, ColorSwatchItem.swatch_size) / 2
            swatch_scene_rect       = QRectF(swatch_position - QPointF(half_swatch_scene_size.width(), half_swatch_scene_size.height()), swatch_scene_size)

            path.addRoundedRect(swatch_scene_rect, ColorSwatchItem.swatch_size / 5, ColorSwatchItem.swatch_size / 5)

        return path

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(self.color_sample.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(), ColorSampleItem.radius, ColorSampleItem.radius)

        painter.setPen(get_item_pen(self))
        painter.drawPath(self.shape())
