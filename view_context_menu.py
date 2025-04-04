from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget, QMenu, QColorDialog, QInputDialog, QDoubleSpinBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QAction
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QMarginsF

import qtawesome as qta

from color_swatch_item import ColorSwatchItem
from edit_color_swatch_dialog import EditColorSwatchDialog

class ViewContextMenu(QMenu):
    def __init__(self, project):
        super().__init__()

        self.project = project

        self.change_background_color_action = QAction("Edit background color...")
        self.change_background_color_action.triggered.connect(self.change_background_color)
        self.change_background_color_action.setIcon(qta.icon("fa5s.palette"))

        self.addAction(self.change_background_color_action)

        self.edit_color_swatch_size_action = QAction("Edit color swatch...")
        self.edit_color_swatch_size_action.triggered.connect(self.edit_color_swatch_size)
        self.edit_color_swatch_size_action.setIcon(qta.icon("fa5s.eye-dropper"))

        self.addAction(self.edit_color_swatch_size_action)

    def change_background_color(self):
        """Changes the background color."""

        def update_background_color(color : QColor):
            self.project.view.set_background_color(color)
            
        if not self.project.color_dialog:
            self.project.color_dialog = QColorDialog(self)
            self.project.color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
            self.project.color_dialog.currentColorChanged.connect(update_background_color)

        self.project.color_dialog.setCurrentColor(self.project.view.backgroundBrush().color())
        self.project.color_dialog.exec()

    def edit_color_swatch_size(self):
        """Edit color swatch parameters."""

        dialog = EditColorSwatchDialog(self.project)

        dialog.exec()

