from PyQt6.QtCore import Qt, QObject, QPointF, pyqtSignal
from PyQt6.QtGui import QColor

from color_swatch_item import ColorSwatchItem

class ColorSwatch(QObject):
    color_swatches      = list()
    position_changed    = pyqtSignal(QPointF)
    anchor_changed      = pyqtSignal(QPointF)
    color_changed       = pyqtSignal(QColor)
    active_changed      = pyqtSignal(bool)

    def __init__(self, project, anchor_alignment : Qt.AlignmentFlag):
        super().__init__()

        ColorSwatch.color_swatches.append(self)

        self.project            = project
        self.anchor_alignment   = anchor_alignment
        self.position           = QPointF()
        self.anchor             = QPointF()
        self.color              = QColor(25, 25, 25)
        self.active             = False
        self.color_sample_link  = None
        self.color_swatch_item  = ColorSwatchItem(self)

    def __del__(self):
        """Remove color swatch from tracking when deleted."""

        if self in ColorSwatch.color_swatches:
            ColorSwatch.color_swatches.remove(self)

    def set_position(self, position : QPointF):
        """Set position in scene coordinates."""

        if position is self.position:
            return
        
        self.position = position

        self.position_changed.emit(self.position)

        anchor_offset = QPointF()
        half_size = ColorSwatchItem.swatch_size / 2

        if self.anchor_alignment == Qt.AlignmentFlag.AlignLeft:
            anchor_offset = QPointF(-half_size, 0)

        if self.anchor_alignment == Qt.AlignmentFlag.AlignRight:
            anchor_offset = QPointF(half_size, 0)

        if self.anchor_alignment == Qt.AlignmentFlag.AlignTop:
            anchor_offset = QPointF(0, -half_size)

        if self.anchor_alignment == Qt.AlignmentFlag.AlignBottom:
            anchor_offset = QPointF(0, half_size)

        self.set_anchor(self.position + anchor_offset)

    def set_anchor(self, anchor : QPointF):
        """Set anchor in scene coordinates."""

        if anchor is self.anchor:
            return
        
        self.anchor = anchor

        self.anchor_changed.emit(self.anchor)

    def activate(self, color_sample_link):
        """Activate the color swatch."""

        self.color_sample_link = color_sample_link

        if not self.active:
            self.active = True

            self.active_changed.emit(self.active)

    def deactivate(self):
        """De-activate the color swatch."""

        self.color_sample_link = None

        if self.active:
            self.active = False

            self.active_changed.emit(self.active)

            self.reset_color()
            
    def set_color(self, color : QColor):
        """Set color."""

        if color is self.color:
            return
        
        self.color = color

        self.color_changed.emit(self.color)

    def reset_color(self):
        """Reset color to default."""

        self.set_color(QColor(25, 25, 25))
