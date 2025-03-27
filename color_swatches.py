from PyQt6.QtWidgets import QLabel, QGraphicsRectItem, QGraphicsLinearLayout, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject

from color_swatch import ColorSwatch

class ColorSwatches(QObject):
    def __init__(self, project):
        super().__init__()

        self.project        = project
        self.items          = list()

        self.left_widget    = QGraphicsWidget()
        self.right_widget   = QGraphicsWidget()
        self.top_widget     = QGraphicsWidget()
        self.bottom_widget  = QGraphicsWidget()

        self.left_layout    = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.right_layout   = QGraphicsLinearLayout(Qt.Orientation.Vertical)
        self.top_layout     = QGraphicsLinearLayout(Qt.Orientation.Horizontal)
        self.bottom_layout  = QGraphicsLinearLayout(Qt.Orientation.Horizontal)

        self.left_layout.setSpacing(ColorSwatch.swatch_spacing)
        self.right_layout.setSpacing(ColorSwatch.swatch_spacing)
        self.top_layout.setSpacing(ColorSwatch.swatch_spacing)
        self.bottom_layout.setSpacing(ColorSwatch.swatch_spacing)

        self.left_widget.setLayout(self.left_layout)
        self.right_widget.setLayout(self.right_layout)
        self.top_widget.setLayout(self.top_layout)
        self.bottom_widget.setLayout(self.bottom_layout)

        self.project.grid_layout.addItem(self.left_widget, 1, 0)
        self.project.grid_layout.addItem(self.right_widget, 1, 2)
        self.project.grid_layout.addItem(self.top_widget, 0, 1)
        self.project.grid_layout.addItem(self.bottom_widget, 2, 1)

    def update(self):
        if not self.project.reference_image:
            return
        
        color_swatch_size               = ColorSwatch.swatch_size + 2 * ColorSwatch.swatch_spacing
        number_of_swatches_horizontal   = self.project.reference_image.size().width() // color_swatch_size
        number_of_swatches_vertical     = self.project.reference_image.size().height() // color_swatch_size

        def add_swatches_to_layout(layout, number_of_swatches):
            layout.addStretch(1)

            for swatch_index in range(number_of_swatches):
                layout.addItem(ColorSwatch())

            layout.addStretch(1)

        add_swatches_to_layout(self.left_layout, number_of_swatches_vertical)
        add_swatches_to_layout(self.right_layout, number_of_swatches_vertical)
        add_swatches_to_layout(self.top_layout, number_of_swatches_horizontal)
        add_swatches_to_layout(self.bottom_layout, number_of_swatches_horizontal)