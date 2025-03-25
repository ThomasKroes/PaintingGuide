from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF

class ColorSwatch(QLabel):
    size                    = 100
    spacing                 = 20
    margin                  = 20
    border_color_active     = Qt.GlobalColor.white
    border_color_inactive   = QColor(90, 90, 90)
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(ColorSwatch.size, ColorSwatch.size)
        
        self.is_active      = False
        self.sampled_color  = QColor(60, 60, 60)
        self.corner_radius  = ColorSwatch.size / 5
        self.border_width   = ColorSwatch.size / 25

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.width(), self.height()).marginsRemoved(QMarginsF(2, 2, 2, 2))
        path = QPainterPath()

        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

        painter.setBrush(QBrush(self.sampled_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        pen = QPen(self.border_color_active if self.is_active else self.border_color_inactive, self.border_width)
        
        pen.setStyle(Qt.PenStyle.SolidLine)

        painter.setPen(pen)
        painter.drawPath(path)

        super().paintEvent(event)

