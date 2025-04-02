import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, pyqtSignal

from graphics_widget import GraphicsWidget
from color_swatch import ColorSwatch
from color_swatch_item import ColorSwatchItem
from color_pie_chart_item import ColorPieChartItem

class ColorSwatches(QObject):
    swatches_changed = pyqtSignal()

    def __init__(self, project):
        super().__init__()

        self.project        = project

        self.left_widget    = GraphicsWidget()
        self.right_widget   = GraphicsWidget()
        self.top_widget     = GraphicsWidget()
        self.bottom_widget  = GraphicsWidget()

        self.left_layout    = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.right_layout   = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.top_layout     = QGraphicsLinearLayout(Qt.Orientation.Horizontal)
        self.bottom_layout  = QGraphicsLinearLayout(Qt.Orientation.Horizontal)

        self.left_layout.setSpacing(ColorSwatchItem.swatch_spacing)
        self.right_layout.setSpacing(ColorSwatchItem.swatch_spacing)
        self.top_layout.setSpacing(ColorSwatchItem.swatch_spacing)
        self.bottom_layout.setSpacing(ColorSwatchItem.swatch_spacing)

        self.left_layout.setContentsMargins(ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing)
        self.right_layout.setContentsMargins(ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing)
        self.top_layout.setContentsMargins(ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing)
        self.bottom_layout.setContentsMargins(ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing, ColorSwatchItem.swatch_spacing)

        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)
        self.top_widget.setLayout(self.top_layout)
        self.bottom_widget.setLayout(self.bottom_layout)

        self.project.grid_layout.addItem(self.left_widget, 1, 0)
        self.project.grid_layout.addItem(self.right_widget, 1, 2)
        self.project.grid_layout.addItem(self.top_widget, 0, 1)
        self.project.grid_layout.addItem(self.bottom_widget, 2, 1)

    def set_color_swatch_size(self, color_swatch_size):
        """Set the color swatch size and re-create the color swatches."""

        self.size = color_swatch_size

        self.update()

        self.swatches_changed.emit()

    def update(self):

        self.clear_layout(self.left_layout)
        self.clear_layout(self.right_layout)
        self.clear_layout(self.top_layout)
        self.clear_layout(self.bottom_layout)

        if not self.project.reference_image:
            return
        
        color_swatch_size               = ColorSwatchItem.swatch_size + 2 * ColorSwatchItem.swatch_spacing
        number_of_swatches_horizontal   = self.project.reference_image.size().width() // int(color_swatch_size)
        number_of_swatches_vertical     = self.project.reference_image.size().height() // int(color_swatch_size)

        def add_swatches_to_layout(layout, number_of_swatches, anchor_alignment):
            layout.addStretch(1)

            for swatch_index in range(number_of_swatches):
                color_swatch = ColorSwatch(self.project, anchor_alignment)
                layout.addItem(color_swatch.color_swatch_item)

            layout.addStretch(1)
            layout.invalidate()

        self.top_widget.update()

        add_swatches_to_layout(self.left_layout, number_of_swatches_vertical, Qt.AlignmentFlag.AlignRight)
        add_swatches_to_layout(self.right_layout, number_of_swatches_vertical, Qt.AlignmentFlag.AlignLeft)
        add_swatches_to_layout(self.top_layout, number_of_swatches_horizontal, Qt.AlignmentFlag.AlignBottom)
        add_swatches_to_layout(self.bottom_layout, number_of_swatches_horizontal, Qt.AlignmentFlag.AlignTop)

    def clear_layout(self, layout):
        """Remove all items from the layout."""

        for item_index in reversed(range(layout.count())):
            layout.removeItem(layout.itemAt(item_index))
            layout.invalidate()

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            pass
            # dict["ColorSwatches"] = {
            #     "Size": self.size,
            #     "Spacing": self.spacing
            # }
        except Exception as e:
            print(f"Unable to save color swatches to dictionary: {e}")
            traceback.print_exc()
    
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""
        
        try:
            # self.size       = dict["ColorSwatches"]["Size"]
            # self.spacing    = dict["ColorSwatches"]["Spacing"]

            self.update()
        except Exception as e:
            print(f"Unable to load color swatches from dictionary: {e}")
            traceback.print_exc()