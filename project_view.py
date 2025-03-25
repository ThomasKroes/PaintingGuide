from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QWheelEvent, QMouseEvent
from PyQt6.QtCore import Qt, QPointF

class ProjectView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self._is_panning = False
        self._pan_start_view_pos = QPointF()  # Start position in VIEW coordinates
        self._zoom_factor = 1.15  # Scale per wheel step

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out when scrolling the mouse wheel"""
        
        zoom_in = event.angleDelta().y() > 0
        scale_factor = self._zoom_factor if zoom_in else 1 / self._zoom_factor

        mouse_scene_pos = self.mapToScene(event.position().toPoint())

        self.scale(scale_factor, scale_factor)

        mouse_view_pos = self.mapFromScene(mouse_scene_pos)
        self.translate(mouse_view_pos.x() - event.position().x(),
                       mouse_view_pos.y() - event.position().y())

    def mousePressEvent(self, event: QMouseEvent):
        """ Start panning only if Alt key is pressed."""

        if event.button() == Qt.MouseButton.LeftButton and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            self._is_panning = True
            self._pan_start_view_pos = event.position()  # Store view position
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Pan the view when dragging with Alt key pressed."""

        if self._is_panning and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            delta = event.position() - self._pan_start_view_pos  # View-space movement
            self._pan_start_view_pos = event.position()  # Update for next move

            # Convert view movement to scene movement (Ensure int values)
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Stop panning when the left mouse button is released."""

        if event.button() == Qt.MouseButton.LeftButton and self._is_panning:
            self._is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)



# # --- Example Usage ---
# app = QApplication([])

# scene = QGraphicsScene()
# scene.addText("Zoom & Pan with Middle Mouse + Scroll")  # Add something to see

# view = PannableZoomableView(scene)
# view.setSceneRect(0, 0, 800, 600)  # Define scene size
# view.show()

# app.exec()
