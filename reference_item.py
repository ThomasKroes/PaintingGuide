from PyQt6.QtWidgets import QLabel, QGraphicsWidget, QGraphicsItem
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF

class ReferenceItem(QGraphicsWidget):
    def __init__(self, project):
        super().__init__()
        
        self.project = project

    def paint(self, painter, option, widget=None):
        
        if self.project.reference_image:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.project.reference_image))

        painter.setPen(Qt.GlobalColor.black)
        painter.drawRect(self.rect())
    
    