from PyQt6.QtCore import Qt, QObject, QPointF, pyqtSignal

from color_swatch_item import ColorSwatchItem

class ColorSwatch(QObject):
    color_swatches      = list()
    position_changed    = pyqtSignal(QPointF)
    anchor_changed      = pyqtSignal(QPointF)

    def __init__(self, project, anchor_alignment : Qt.AlignmentFlag):
        super().__init__()

        ColorSwatch.color_swatches.append(self)

        self.project            = project
        self.anchor_alignment   = anchor_alignment
        self.position           = QPointF()
        self.anchor             = QPointF()
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

    def set_anchor(self, anchor : QPointF):
        """Set anchor in scene coordinates."""

        if anchor is self.anchor:
            return
        
        self.anchor = anchor

        self.anchor_changed.emit(self.anchor)
