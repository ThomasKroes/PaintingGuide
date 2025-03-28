from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject

from color_swatch_item import ColorSwatchItem
from reference_label import ReferenceLabel

class ProjectWidget(QWidget):
    def __init__(self, reference_image_file_path, project):
        super().__init__()

        self.project    = project
        grid_layout     = QGridLayout()

        grid_layout.setContentsMargins(10, 10, 10, 10)
        grid_layout.setSpacing(0)

        self.top_layout     = QHBoxLayout()
        self.bottom_layout  = QHBoxLayout()
        self.left_layout    = QVBoxLayout()
        self.right_layout   = QVBoxLayout()

        self.border_layouts = [self.top_layout, self.bottom_layout, self.left_layout, self.right_layout]
        
        grid_layout.addLayout(self.top_layout, 0, 1)
        grid_layout.addLayout(self.bottom_layout, 2, 1)
        grid_layout.addLayout(self.left_layout, 1, 0)
        grid_layout.addLayout(self.right_layout, 1, 2)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(2, 1)

        for border_layout in self.border_layouts:
            border_layout.setSpacing(ColorSwatchItem.spacing)
            border_layout.setContentsMargins(ColorSwatchItem.margin, ColorSwatchItem.margin, ColorSwatchItem.margin, ColorSwatchItem.margin)

        grid_layout.setAlignment(self.left_layout, Qt.AlignmentFlag.AlignTop)

        self.setLayout(grid_layout)
        self.set_reference_image_file_path(reference_image_file_path)

    def populate_color_swatches_layout(self, layout, num_color_swatches, alignment):
        """Populate left, right top or bottom layout with color swatches."""

        layout.addStretch(1)

        for i in range(num_color_swatches):
            color_swatch = ColorSwatchItem()

            layout.addWidget(color_swatch)
            layout.setAlignment(color_swatch, alignment)

        layout.addStretch(1)

    def add_color_swatches(self):
        """ Add color swatches around the reference image."""

        if self.project.reference_image:
            img_width   = self.project.reference_image.width()
            img_height  = self.project.reference_image.height()
            size        = ColorSwatchItem.size + ColorSwatchItem.spacing

            num_top_bottom = (img_width // size)
            num_left_right = (img_height // size)

            self.populate_color_swatches_layout(self.top_layout, num_top_bottom, Qt.AlignmentFlag.AlignBottom)
            self.populate_color_swatches_layout(self.bottom_layout, num_top_bottom, Qt.AlignmentFlag.AlignTop)
            self.populate_color_swatches_layout(self.left_layout, num_left_right, Qt.AlignmentFlag.AlignRight)
            self.populate_color_swatches_layout(self.right_layout, num_left_right, Qt.AlignmentFlag.AlignLeft)

    def set_reference_image_file_path(self, reference_image_file_path):
        """Set the reference image file path."""

        self.add_color_swatches()