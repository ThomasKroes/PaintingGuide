from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QBrush, QColor, QPainter, QPixmap
from PyQt6.QtCore import Qt, QPointF, QRect

from magic_lens_item import MagicLensItem
from color_sample import ColorSample
from view_context_menu import ViewContextMenu
from common import *

class ProjectView(QGraphicsView):
    def __init__(self, project):
        super().__init__(project.scene)
        
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.project                = project
        self.is_panning             = False
        self.pan_start_view_pos     = QPointF()
        self.zoom_factor            = 1.15
        self.magic_lens_item        = None
        self.magnification_factor   = 2

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
                ColorSample.create_from_scene_position(self.project, self.mapToScene(event.pos()).toPoint())

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
