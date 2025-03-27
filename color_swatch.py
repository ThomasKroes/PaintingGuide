from PyQt6.QtWidgets import QLabel, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF

class ColorSwatch(QGraphicsWidget):
    swatch_size             = 100
    swatch_spacing          = 20
    margin                  = 20
    border_color_active     = Qt.GlobalColor.white
    border_color_inactive   = QColor(90, 90, 90)
    
    def __init__(self):
        super().__init__()

        self.resize(ColorSwatch.swatch_size, ColorSwatch.swatch_size)
        self.setMinimumSize(ColorSwatch.swatch_size, ColorSwatch.swatch_size)
        self.setMaximumSize(ColorSwatch.swatch_size, ColorSwatch.swatch_size)

        self.is_active      = False
        self.sampled_color  = QColor(60, 60, 60)
        self.corner_radius  = ColorSwatch.swatch_size / 5
        self.border_width   = ColorSwatch.swatch_size / 25

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(0, 0, self.size().width(), self.size().height()).marginsRemoved(QMarginsF(2, 2, 2, 2))
        path = QPainterPath()

        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)

        painter.setBrush(QBrush(self.sampled_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)
        
        pen = QPen(self.border_color_active if self.is_active else self.border_color_inactive, self.border_width)
        
        pen.setStyle(Qt.PenStyle.SolidLine)

        painter.setPen(pen)
        painter.drawPath(path)

