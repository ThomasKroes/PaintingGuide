from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QBrush, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QPointF, QRect

from magic_lens_item import MagicLensItem
from color_sample_item import ColorSampleItem

class ProjectView(QGraphicsView):
    def __init__(self, project):
        super().__init__(project.scene)
        
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        self.project                = project
        self.is_panning             = False
        self.pan_start_view_pos     = QPointF()
        self.zoom_factor            = 1.15
        self.magic_lens_item         = None
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

        if event.button() == Qt.MouseButton.LeftButton:
            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
                self.is_panning            = True
                self.pan_start_view_pos    = event.position()

                self.setCursor(Qt.CursorShape.ClosedHandCursor)

            if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier:
                self.project.add_color_sample_from_scene_position(self.mapToScene(event.pos()).toPoint())

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Pan the view when dragging with Alt key pressed."""

        if self.is_panning and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            delta = event.position() - self.pan_start_view_pos

            self.pan_start_view_pos = event.position()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))
        else:

            # if self.project.reference_image:
            #     project_widget_proxy_local_pos = self.widget.project.widget_proxy.mapFromScene(self.mapToScene(event.pos()))
            #     pixmap_position = self.widget.reference_label.mapFromParent(project_widget_proxy_local_pos)

                

            #     if self.magic_lens_item:
            #         self.scene().removeItem(self.magic_lens_item)

            #     self.magic_lens_item = MagicLensItem(self.project, pixmap_position)

            #     self.scene().addItem(self.magic_lens_item)

            #     self.update()

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
