from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QSizeF, QPointF, QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QGraphicsItem

from enum import Enum

class ItemType(Enum):
    ColorSwatch = 1
    ColorSample = 2
    ColorSampleLink = 3

class ItemState(Enum):
    Normal = 1
    Hover = 2
    Selected = 3
    Active = 4

def get_item_pen(item : QGraphicsItem):
    """Get border width for item."""

    from color_sample_item import ColorSampleItem
    from color_swatch import ColorSwatchItem
    from reference_item import ReferenceItem
    from color_sample_link_item import ColorSampleLinkItem

    if isinstance(item, ColorSampleItem):
        if item.isSelected():
            return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 12))
        
        return QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 6)
    
    if isinstance(item, ColorSwatchItem):
        if item.isSelected():
            return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 12))
        
        if item.color_swatch.active:
            return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 12))
        
        return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Dark), 5))

    if isinstance(item, ReferenceItem):
        return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 5))
    
    if isinstance(item, ColorSampleLinkItem):
        return QPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), 12))
    
    print("No matching pen found...")

    return QPen()