from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QInputDialog, QVBoxLayout, QDoubleSpinBox, QDialogButtonBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer

def color_to_dict(color : QColor):
    """Get a dictionary from a Qt color."""
    
    return {
        "Red": color.red(),
        "Green": color.green(),
        "Blue": color.blue()
    }

def color_from_dict(dict : dict):
    """Get a Qt color from a dictionary."""

    try:
        return QColor(dict["Red"], dict["Green"], dict["Blue"])
    except:
        return QColor()
