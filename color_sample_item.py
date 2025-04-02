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

        self.setZValue(100)

        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsScenePositionChanges)
        
        self.color_sample.position_changed.connect(self.position_changed)
        self.color_sample.color_changed.connect(self.update)

        self.setGeometry(self.boundingRect())
        
        self.update()
        
    def __debug_print__(self, message : str):
        """Print a nicely formatted debug message."""

        if self.verbose:
            print(f"{ __class__.__name__ }: { message }")

    def __del__(self):
        """Remove color sample item from tracking when deleted."""

        self.__debug_print__("Delete")

    def position_changed(self):
        """Invoked when the color sample position has changed."""

        self.setPos(self.color_sample.position)

        # print(f"Position: { qpointf_to_string(self.color_sample.position) }")

        # self.setGeometry(self.boundingRect())
    # def mousePressEvent(self, event):
    #     """Invoked when the mouse button is pressed."""

    #     print("----")
    #     self.__debug_print__("Mouse Pressed")
        
    #     super().mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     """Invoked when the mouse is moved."""

    #     self.__debug_print__("Mouse Moved")

    #     super().mouseMoveEvent(event)  # Default handling

    # def mouseReleaseEvent(self, event):
    #     """Invoked when the mouse button is released."""

    #     self.__debug_print__("Mouse Released")

    #     super().mouseReleaseEvent(event)
        
    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.color_sample.set_position(self.scenePos())

        # if change == QGraphicsEllipseItem.GraphicsItemChange.ItemSelectedChange:
        #     self.update()

        # if change == QGraphicsEllipseItem.GraphicsItemChange.ItemSelectedHasChanged:
        #     print("ItemSelectedHasChanged")
        #     self.update()

        return super().itemChange(change, value)
    
    # def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
    #     """Display a context menu at the cursor position."""

    #     color_sample_context_menu = ColorSampleContextMenu(self.color_sample)

    #     color_sample_context_menu.exec(event.screenPos())

    def boundingRect(self):
        """Return the bounding rectangle for the item."""

        center  = self.mapFromScene(self.color_sample.position)
        margin  = 10
        margins = QMarginsF(margin, margin, margin, margin)

        return QRectF(QPointF() - QPointF(ColorSampleItem.radius, ColorSampleItem.radius), 2 * QSizeF(ColorSampleItem.radius, ColorSampleItem.radius)).marginsAdded(margins)
    
    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # center = self.boundingRect().center()# self.mapFromScene(self.color_sample.position)

        painter.setBrush(QBrush(self.color_sample.color))
        painter.setPen(get_item_pen(self))
        painter.drawEllipse(QPointF(), ColorSampleItem.radius, ColorSampleItem.radius)

        # painter.setBrush(Qt.BrushStyle.NoBrush)
        # painter.setPen(QPen(QColor(1, 0, 0), 5))
        # painter.drawRect(self.boundingRect())