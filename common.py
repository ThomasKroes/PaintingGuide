from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QInputDialog, QVBoxLayout, QDoubleSpinBox, QDialogButtonBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer

def qcolor_to_dict(color : QColor):
    """Get a dictionary from a QColor."""
    
    return {
        "Red": color.red(),
        "Green": color.green(),
        "Blue": color.blue()
    }

def qcolor_from_dict(dict : dict):
    """Get a QColor from a dictionary."""

    try:
        return QColor(dict["Red"], dict["Green"], dict["Blue"])
    except:
        return QColor()
    
def qcolor_to_rgb_string(color : QColor):
    """Get RGB string from QColor."""

    return f"rgb({ str(color.red()) }, { str(color.green()) }, { str(color.blue()) })"

def qcolor_to_hsl_string(color : QColor):
    """Get HSL string from QColor."""

    return f"hsl({ str(color.hue()) }, { str(color.saturation()) }, { str(color.lightness()) })"

def qpointf_to_dict(point : QPointF):
    """Get a dictionary from a QPointF."""
    
    return {
        "X": point.x(),
        "Y": point.y()
    }

def qpointf_to_string(point : QPointF):
    """Get point string from QPointF."""

    return f"({ '{:.2f}'.format(point.x()) }, { '{:.2f}'.format(point.y()) })"

def qpointf_from_dict(dict : dict):
    """Get a QPointF from a dictionary."""

    try:
        return QPointF(dict["X"], dict["Y"])
    except:
        return QPointF()

