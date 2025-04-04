from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QRectF, QMarginsF

from graphics_widget import GraphicsWidget
from color_swatch_item import ColorSwatchItem

from styling import *

class ReferenceItem(GraphicsWidget):
    def __init__(self, project):
        super().__init__()
        
        self.setZValue(-100)

        self.project = project

        self.setAcceptHoverEvents(True)
        
        self.setFlag(GraphicsWidget.GraphicsItemFlag.ItemSendsGeometryChanges)
        # self.setGeometry(self.boundingRect())

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Pan the view when dragging with Alt key pressed."""

        print("--------")

    def boundingRect(self):
        """Return the bounding rectangle for the item."""

        return QRectF(QPointF(), self.project.reference_image.size().toSizeF())
                      
    def paint(self, painter, option, widget=None):
        """Override the paint method for customization."""
        
        if self.project.reference_image:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.project.reference_image))

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(get_item_pen(self))
        painter.drawRect(self.rect())
   
    