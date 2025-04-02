from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QSizeF, QPointF
from PyQt6.QtWidgets import QGraphicsItem

from graphics_widget import GraphicsWidget
from styling import *

class ColorSwatchItem(GraphicsWidget):
    swatch_size                 = 250
    swatch_spacing              = swatch_size / 5
    margin                      = 20
    items                       = list()
    background_color_inactive   = QColor(60, 60, 60)

    def __init__(self, color_swatch):
        super().__init__()

        ColorSwatchItem.items.append(self)
        
        self.set_fixed_size(QSizeF(ColorSwatchItem.swatch_size, ColorSwatchItem.swatch_size))

        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsScenePositionChanges)
        
        self.color_swatch           = color_swatch
        self.corner_radius          = ColorSwatchItem.swatch_size / 5
        self.border_width           = ColorSwatchItem.swatch_size / 25
        self.anchor_position_scene  = QPointF()

        self.color_swatch.color_changed.connect(self.update)
        self.color_swatch.active_changed.connect(self.update)

    def itemChange(self, change, value):
        """Invoked when the item changes."""

        anchor_position_scene = QPointF()

        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.color_swatch.anchor_alignment is Qt.AlignmentFlag.AlignLeft:
                anchor_position_scene = QPointF(self.rect().left(), self.rect().center().y())

            if self.color_swatch.anchor_alignment is Qt.AlignmentFlag.AlignRight:
                anchor_position_scene = QPointF(self.rect().right(), self.rect().center().y())

            if self.color_swatch.anchor_alignment is Qt.AlignmentFlag.AlignTop:
                anchor_position_scene = QPointF(self.rect().center().x(), self.rect().top())

            if self.color_swatch.anchor_alignment is Qt.AlignmentFlag.AlignBottom:
                anchor_position_scene = QPointF(self.rect().center().x(), self.rect().bottom())

            self.color_swatch.set_anchor(self.mapToScene(anchor_position_scene))

        return super().itemChange(change, value)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.size().width(), self.size().height()).marginsRemoved(QMarginsF(2, 2, 2, 2))
        path = QPainterPath()

        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

        painter.setBrush(QBrush(self.color_swatch.color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        # border_color = get_border_color(ItemType.ColorSwatch, ItemState.Selected if self.isSelected() else ItemState.Normal)
        # border_width = get_border_width(ItemType.ColorSwatch, ItemState.Selected if self.isSelected() else ItemState.Normal)

        # pen = QPen(border_color, border_width)
        
        # pen.setStyle(Qt.PenStyle.SolidLine)

        painter.setPen(get_item_pen(self))
        painter.drawPath(path)

