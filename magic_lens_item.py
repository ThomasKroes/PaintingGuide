import sys

from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QPixmap, QPainter, QImage, QColor, QBrush
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsWidget, QLabel, QGraphicsProxyWidget, QGraphicsItem
from PyQt6.QtCore import Qt, QPointF, QRect, QRectF, QSize

class MagicLensItem(QGraphicsItem):
    def __init__(self, project, center, magnification_factor=2, parent=None):
        super().__init__(parent)

        self.project                = project
        self.center                 = center
        self.magnification_factor   = magnification_factor
        self.zoom_size              = 50

    def boundingRect(self):
        return QRectF(self.center.x() - 50, self.center.y() - 50, 100, 100)

    def paint(self, painter, option, widget):
        if not self.project.reference_image:
            return
        
        return
        # Extract the mouse position in the pixmap coordinates (scene coordinates)
        scene_pos = self.center
        mouse_x = int(scene_pos.x())
        mouse_y = int(scene_pos.y())

        # Define the zoom area (rectangular region around the mouse)
        rect = QRect(mouse_x - self.zoom_size, mouse_y - self.zoom_size, 2 * self.zoom_size, 2 * self.zoom_size)

        # Ensure the rect stays within the pixmap's bounds
        rect = rect.intersected(QRect(0, 0, self.project.pixmap.width(), self.project.pixmap.height()))

        # Convert pixmap to QImage to access pixel data
        image = self.project.pixmap.toImage()
        cropped_image = image.copy(rect)

        # Scale the cropped area to create the zoom effect
        zoomed_image = cropped_image.scaled(cropped_image.size() * self.magnification_factor)

        # Draw the zoomed image inside the circle
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # Get the position of the item in the scene coordinate system
        item_pos = self.scenePos()  # Get the top-left corner position of the item in the scene

        # Compute the target rect by adding the item’s position to the desired bounding rect
        target_rect = self.boundingRect().toRect()

        # Offset the target rectangle by the item’s position
        target_rect.moveTopLeft(target_rect.topLeft() + item_pos.toPoint()) 

        # Draw the zoomed image at the correct position
        painter.drawPixmap(QRect(self.center, QSize(self.zoom_size, self.zoom_size)), QPixmap.fromImage(zoomed_image))