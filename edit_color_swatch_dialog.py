from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication, QInputDialog, QVBoxLayout, QDoubleSpinBox, QDialogButtonBox, QDialog, QGridLayout, QSpacerItem
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer, QSize

import qtawesome as qta

class EditColorSwatchDialog(QDialog):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Edit color swatch parameters")
        self.setWindowIcon(qta.icon("fa5s.eye-dropper"))

        self.project = project
        
        layout = QGridLayout(self)

        self.label = QLabel()
        
        self.label.setText("Swatch size:")

        layout.addWidget(self.label, 0, 0)

        self.color_swatch_size_spinbox = QDoubleSpinBox()
        
        self.color_swatch_size_spinbox.setDecimals(1)
        self.color_swatch_size_spinbox.setRange(0.0, 100.0)
        self.color_swatch_size_spinbox.setSuffix(" px")
        self.color_swatch_size_spinbox.setValue(100.0)

        self.color_swatch_size_spinbox.valueChanged.connect(self.update_color_swatches)

        layout.addWidget(self.color_swatch_size_spinbox, 0, 1)
        layout.setRowStretch(1, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        
        layout.addWidget(self.buttons, 2, 0, 1, 2)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def update_color_swatches(self, color_swatch_size):
        """Create new layout with swatches."""

        self.project.color_swatches.set_color_swatch_size(color_swatch_size)

    def sizeHint(self):
        return QSize(300, 80)