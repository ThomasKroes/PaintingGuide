import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QMarginsF

from graphics_widget import GraphicsWidget
from color_swatch_item import ColorSwatchItem
from color_pie_chart_item import ColorPieChartItem

class ColorSwatch(QObject):
    color_swatches = list()

    def __init__(self, color_swatch):
        super().__init__()

        ColorSwatch.color_swatches.append(self)

        self.color_swatch       = color_swatch
        self.color_swatch_item  = ColorSwatchItem(self)

    def __del__(self):
        """Remove color swatch from tracking when deleted."""

        if self in ColorSwatch.color_swatches:
            ColorSwatch.color_swatches.remove(self)