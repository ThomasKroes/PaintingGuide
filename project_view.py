from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QBrush, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QPointF, QRect

from magic_lens_item import MagicLensItem

class ProjectView(QGraphicsView):
    def __init__(self, scene, project_widget):
        super().__init__(scene)
        
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        self.project_widget         = project_widget
        self.is_panning             = False
        self.pan_start_view_pos     = QPointF()
        self.zoom_factor            = 1.15
        self.magnified_item         = None
        self.magnification_factor   = 2

    def wheelEvent(self, event: QWheelEvent):
        """ Zoom in/out when scrolling the mouse wheel"""
        
        zoom_in         = event.angleDelta().y() > 0
        scale_factor    = self.zoom_factor if zoom_in else 1 / self.zoom_factor

        mouse_scene_pos = self.mapToScene(event.position().toPoint())

        self.scale(scale_factor, scale_factor)

        mouse_view_pos = self.mapFromScene(mouse_scene_pos)

        self.translate(mouse_view_pos.x() - event.position().x(), mouse_view_pos.y() - event.position().y())

    def mousePressEvent(self, event: QMouseEvent):
        """ Start panning only if Alt key is pressed."""

        if event.button() == Qt.MouseButton.LeftButton and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            self.is_panning            = True
            self.pan_start_view_pos    = event.position()

            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Pan the view when dragging with Alt key pressed."""

        if self.is_panning and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            delta = event.position() - self.pan_start_view_pos

            self.pan_start_view_pos = event.position()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))
        else:

            if not self.project_widget.pixmap.isNull():
                project_widget_proxy_local_pos = self.project_widget.project.widget_proxy.mapFromScene(self.mapToScene(event.pos()))
                pixmap_position = self.project_widget.reference_label.mapFromParent(project_widget_proxy_local_pos)

                if self.magnified_item:
                    self.scene().removeItem(self.magnified_item)

                self.magnified_item = MagicLensItem(event.position().toPoint(), self.project_widget.pixmap)

                self.scene().addItem(self.magnified_item)

                self.update()

            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Stop panning when the left mouse button is released."""

        if event.button() == Qt.MouseButton.LeftButton and self.is_panning:
            self.is_panning = False
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
