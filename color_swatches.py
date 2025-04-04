import traceback

from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPointF, QMarginsF, QObject, pyqtSignal

from graphics_widget import GraphicsWidget
from color_swatch import ColorSwatch
from color_swatch_item import ColorSwatchItem
from color_pie_chart_item import ColorPieChartItem

class ColorSwatches(QObject):
    swatches_changed = pyqtSignal()

    def __init__(self, project):
        super().__init__()

        self.project        = project

    def set_color_swatch_size(self, color_swatch_size):
        """Set the color swatch size and re-create the color swatches."""

        self.size = color_swatch_size

        self.update()

        self.swatches_changed.emit()

    def update(self):

        if not self.project.reference_image:
            return
        
        spacing = 100
        swatch_size                     = ColorSwatchItem.swatch_size
        half_swatch_size                = swatch_size / 2
        reference_width                 = self.project.reference_image.size().width()
        reference_height                = self.project.reference_image.size().height()
        number_of_swatches_horizontal   = reference_width // int(swatch_size + spacing)
        number_of_swatches_vertical     = reference_height // int(swatch_size + spacing)
        
        reference_image = self.project.reference_image

        def add_swatches(number_of_swatches, orientation):
            total_spacing   = spacing * max(1, number_of_swatches - 1)
            total_swatches  = number_of_swatches * swatch_size

            if orientation == Qt.Orientation.Vertical:
                offset = half_swatch_size + (reference_image.height() - total_spacing - total_swatches) / 2

                for swatch_index in range(number_of_swatches):
                    left_swatch     = ColorSwatch(self.project, Qt.AlignmentFlag.AlignRight)
                    right_swatch    = ColorSwatch(self.project, Qt.AlignmentFlag.AlignLeft)
                    position_y      = offset + swatch_index * (swatch_size + spacing)

                    left_swatch.set_position(QPointF(-half_swatch_size - spacing, position_y))
                    right_swatch.set_position(QPointF(reference_width + spacing + half_swatch_size, position_y))

                    self.project.scene.addItem(left_swatch.color_swatch_item)
                    self.project.scene.addItem(right_swatch.color_swatch_item)
                
            if orientation == Qt.Orientation.Horizontal:
                offset = half_swatch_size + (reference_image.width() - total_spacing - total_swatches) / 2

                for swatch_index in range(number_of_swatches):
                    top_swatch      = ColorSwatch(self.project, Qt.AlignmentFlag.AlignBottom)
                    bottom_swatch   = ColorSwatch(self.project, Qt.AlignmentFlag.AlignTop)
                    position_x      = offset + swatch_index * (swatch_size + spacing)

                    top_swatch.set_position(QPointF(position_x, -spacing - half_swatch_size))
                    bottom_swatch.set_position(QPointF(position_x, reference_height + spacing + half_swatch_size))

                    self.project.scene.addItem(top_swatch.color_swatch_item)
                    self.project.scene.addItem(bottom_swatch.color_swatch_item)

        add_swatches(number_of_swatches_horizontal, Qt.Orientation.Horizontal)
        add_swatches(number_of_swatches_vertical, Qt.Orientation.Vertical)
        
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