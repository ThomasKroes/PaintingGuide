import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette, QFont
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF

from graphics_widget import GraphicsWidget
from common import *
from styling import *

class ColorSampleLinkItem(GraphicsWidget):
    def __init__(self, color_sample_link):
        super().__init__()

        self.color_sample_link  = color_sample_link
        self.line               = QLineF()
        self.verbose            = True

        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemIsSelectable)

        self.color_sample_link.visible_changed.connect(self.update_visibility)

        self.setOpacity(0)
        self.setZValue(3)
        
    def remove(self):
        """Remove the color sample link item."""

        self.print("Remove")

        self.color_sample_link.color_sample.project.scene.removeItem(self)

        self.color_sample_link.visible_changed.disconnect(self.update_visibility)
        
        self.color_sample_link = None

        del self
    
    def set_line(self, line):
        """Set link line segment."""

        self.line = line

        self.update()

    def update_visibility(self):
        """Update the visibility of the link."""

        if self.color_sample_link.visible:
            self.setOpacity(1)
        else:
            self.setOpacity(0)

        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemSelectedHasChanged:
            self.color_sample_link.color_sample.set_selected(self.isSelected())
            
        return super().itemChange(change, value)
    
    def boundingRect(self):
        """Return the bounding rectangle for the item."""

        margin  = 50
        margins = QMarginsF(margin, margin, margin, margin)

        return QRectF(self.line.p1(), self.line.p2()).normalized().marginsAdded(margins)
    
    def paint(self, painter: QPainter, option, widget=None):
        if not self.color_sample_link.visible:
            return
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setPen(get_item_pen(self))
        painter.drawLine(self.line)

    # def animate(self, value):
    #     self.setOpacity(value)

    # def fade_in(self):
    #     """Animate fade in."""
        
    #     self.animation.setDirection(QPropertyAnimation.Direction.Forward)
    #     self.animation.start()

    # def fade_out(self):
    #     """Animate fade out."""

    #     self.animation.setDirection(QPropertyAnimation.Direction.Backward)
    #     self.animation.start()

    

        