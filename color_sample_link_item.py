import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer, QPropertyAnimation

class ColorSampleLinkItem(QGraphicsLineItem):
    def __init__(self, color_sample):
        super().__init__()

        self.setPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 4))
        