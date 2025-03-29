from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QSizeF, QPointF
from PyQt6.QtWidgets import QGraphicsItem

from graphics_widget import GraphicsWidget

class ColorPieChartItem(GraphicsWidget):
    def __init__(self):
        super().__init__()

        self.color = QColor(60, 60, 60)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define rectangle for pie chart
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

        # Get RGB values
        r, g, b = self.color.red(), self.color.green(), self.color.blue()
        total = r + g + b
        if total == 0:  # Avoid division by zero
            return

        # Convert RGB values to angles (full circle = 360 * 16 in Qt)
        r_angle = int(360 * 16 * (r / total))
        g_angle = int(360 * 16 * (g / total))
        b_angle = 360 * 16 - (r_angle + g_angle)  # Ensure sum is exactly 360*16

        # Start drawing from 0 degrees
        start_angle = 0

        # Draw Red Slice
        painter.setBrush(QColor("red"))
        painter.drawPie(rect, start_angle, r_angle)
        start_angle += r_angle

        # Draw Green Slice
        painter.setBrush(QColor("green"))
        painter.drawPie(rect, start_angle, g_angle)
        start_angle += g_angle

        # Draw Blue Slice
        painter.setBrush(QColor("blue"))
        painter.drawPie(rect, start_angle, b_angle)
