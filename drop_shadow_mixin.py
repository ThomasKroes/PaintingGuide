from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class DropShadowMixin():
    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(8)
        shadow.setOffset(4, 4)
        shadow.setColor(QColor(0, 0, 0, 100))

        self.setGraphicsEffect(shadow)