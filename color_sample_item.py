import traceback

from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneContextMenuEvent, QGraphicsWidget
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtCore import Qt, QPointF

from graphics_widget import GraphicsWidget
from color_sample_context_menu import ColorSampleContextMenu
from common import *
from styling import *

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class ColorSampleItem(GraphicsWidget):
    radius  = 50
    items   = list()

    def __init__(self, color_sample):
        super().__init__()
        
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

        margin  = 10
        margins = QMarginsF(margin, margin, margin, margin)

        return QRectF(QPointF() - QPointF(ColorSampleItem.radius, ColorSampleItem.radius), 2 * QSizeF(ColorSampleItem.radius, ColorSampleItem.radius)).marginsAdded(margins)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QBrush(self.color_sample.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(), ColorSampleItem.radius, ColorSampleItem.radius)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(get_item_pen(self))
        painter.drawEllipse(QPointF(), ColorSampleItem.radius, ColorSampleItem.radius)