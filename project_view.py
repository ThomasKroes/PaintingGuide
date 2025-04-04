from PyQt6.QtWidgets import QApplication, QGraphicsView
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QPointF, pyqtSignal

from color_sample import ColorSample
from view_context_menu import ViewContextMenu

from common import *

class ProjectView(QGraphicsView):
    zoom_factor_changed = pyqtSignal(float)

    def __init__(self, project):
        super().__init__(project.scene)
        
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # self.customContextMenuRequested.connect(self.show_context_menu)

        self.project                = project
        self.is_panning             = False
        self.pan_start_view_pos     = QPointF()
        self.zoom_factor            = 1.15
        self.magic_lens_item        = None
        self.magnification_factor   = 2
        self.zoom_level             = 100

        self.set_background_color(QColor(25, 25, 25))

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
                ColorSample.create_from_scene_position(self.project, self.mapToScene(event.pos()))

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ Pan the view when dragging with Alt key pressed."""

        if self.is_panning and QApplication.keyboardModifiers() & Qt.KeyboardModifier.AltModifier:
            delta = event.position() - self.pan_start_view_pos

            self.pan_start_view_pos = event.position()

            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - int(delta.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - int(delta.y()))

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ Stop panning when the left mouse button is released."""

        if event.button() == Qt.MouseButton.LeftButton and self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)
    
    def zoom_in(self):
        """Zoom in by 10%."""

        self.zoom_level *= 1.1
        self.update_zoom()

    def zoom_out(self):
        """Zoom out by 10%."""

        self.zoom_level *= 0.9
        self.update_zoom()
        
    def reset_zoom(self):
        """Reset zoom to 100%."""

        self.zoom_level = 100
        self.update_zoom()

    def update_zoom(self):
        """Update the zoom level based on the scene size and the current view size."""

        # Calculate the bounding rectangle of the scene
        scene_rect = self.scene().sceneRect()
        
        # Calculate the scale factor based on the view size and scene size
        view_width = self.viewport().width()
        view_height = self.viewport().height()

        scale_x = view_width / scene_rect.width()  # Horizontal scale
        scale_y = view_height / scene_rect.height()  # Vertical scale

        # Apply the appropriate scaling (we use the smaller scale to fit the whole scene in view)
        scale_factor = min(scale_x, scale_y)

        # Set the scale factor as the zoom factor
        self.setTransform(self.transform().scale(scale_factor, scale_factor))

        # Update the zoom level based on the scale factor
        self.zoom_level = int(scale_factor * 100)

        self.zoom_factor_changed.emit(self.zoom_level)

    def zoom_extents(self):
        """Zoom the view to fit the entire scene."""

        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)
        self.update_zoom()
                
    def show_context_menu(self, pos):
        """Display a context menu at the cursor position."""

        view_context_menu = ViewContextMenu(self.project)

        view_context_menu.exec(self.mapToGlobal(pos))

    def set_background_color(self, background_color : QColor):
        """Set background color of the view."""

        self.setBackgroundBrush(background_color)

    def to_dict(self):
        """Convert the reference item properties to a dictionary."""

        return {
            "BackgroundColor": qcolor_to_dict(self.background_color),
        }

    def from_dict(self, dict):
        """Serialize the reference item from JSON."""

        self.background_color = qcolor_from_dict(dict["BackgroundColor"])
