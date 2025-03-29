from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QSizeF, QPointF
from PyQt6.QtWidgets import QGraphicsItem

from graphics_widget import GraphicsWidget

class ColorSwatchItem(GraphicsWidget):
    swatch_size                 = 100
    swatch_spacing              = 20
    margin                      = 20
    border_color_active         = Qt.GlobalColor.white
    border_color_inactive       = QColor(90, 90, 90)
    items                       = list()
    background_color_inactive   = QColor(60, 60, 60)

    def __init__(self, anchor_alignment : Qt.AlignmentFlag):
        super().__init__()

        ColorSwatchItem.items.append(self)
        
        self.set_fixed_size(QSizeF(ColorSwatchItem.swatch_size, ColorSwatchItem.swatch_size))

        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsScenePositionChanges)

        self.anchor_alignment       = anchor_alignment
        self.is_active              = False
        self.sample_color           = QColor(60, 60, 60)
        self.corner_radius          = ColorSwatchItem.swatch_size / 5
        self.border_width           = ColorSwatchItem.swatch_size / 25
        self.color_sample_item      = None
        self.anchor_position_scene  = QPointF()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            if self.anchor_alignment is Qt.AlignmentFlag.AlignLeft:
                self.anchor_position_scene = QPointF(self.rect().left(), self.rect().center().y())

            if self.anchor_alignment is Qt.AlignmentFlag.AlignRight:
                self.anchor_position_scene = QPointF(self.rect().right(), self.rect().center().y())

            if self.anchor_alignment is Qt.AlignmentFlag.AlignTop:
                self.anchor_position_scene = QPointF(self.rect().center().x(), self.rect().top())

            if self.anchor_alignment is Qt.AlignmentFlag.AlignBottom:
                self.anchor_position_scene = QPointF(self.rect().center().x(), self.rect().bottom())

            self.anchor_position_scene = self.mapToScene(self.anchor_position_scene)

        return super().itemChange(change, value)

    def __del__(self):
        """Remove item from tracking when deleted."""

        if self.color_sample_item:
            self.color_sample_item.disconnect_from_color_swatch_item()

    def connect_to_color_sample_item(self, color_sample_item):
        """Connect to color sample item."""

        self.color_sample_item  = color_sample_item
        self.is_active          = True

    def disconnect_from_color_sample_item(self):
        """Disconnect from color sample item."""

        self.sample_color       = ColorSwatchItem.background_color_inactive
        self.color_sample_item  = None
        self.is_active          = False

        self.update()

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.size().width(), self.size().height()).marginsRemoved(QMarginsF(2, 2, 2, 2))
        path = QPainterPath()

        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

        painter.setBrush(QBrush(self.sample_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        pen = QPen(self.border_color_active if self.is_active else self.border_color_inactive, self.border_width)
        
        pen.setStyle(Qt.PenStyle.SolidLine)

        painter.setPen(pen)
        painter.drawPath(path)

