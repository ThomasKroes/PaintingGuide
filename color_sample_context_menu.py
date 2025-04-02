from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget, QMenu, QColorDialog, QInputDialog, QDoubleSpinBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QAction
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QMarginsF

import qtawesome as qta

class ColorSampleContextMenu(QMenu):
    def __init__(self, color_sample):
        super().__init__()

        self.color_sample = color_sample

        self.remove_color_sample_action = QAction("Remove")
        self.remove_color_sample_action.triggered.connect(self.remove_color_sample)
        self.remove_color_sample_action.setIcon(qta.icon("fa5s.trash"))

        self.addAction(self.remove_color_sample_action)

    def remove_color_sample(self):
        """Removes the color sample."""

        self.color_sample.remove()

