from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QApplication
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QVector2D, QPalette
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF, QLineF, QTimer

from color_swatch_item import ColorSwatchItem

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class Link(QObject):
    def __init__(self, color_sample_item, color_swatch_item):
        super().__init__()

        self.color_sample_item      = color_sample_item
        self.color_swatch_item      = color_swatch_item
        self.color_sample_center    = QVector2D(self.color_sample_item.anchor_position_scene)
        self.color_swatch_center    = QVector2D(self.color_swatch_item.anchor_position_scene)
        self.distance               = (self.color_sample_center - self.color_swatch_center).length()

class LinkItem(QGraphicsLineItem):
    border_thickness    = 4
    border_color        = ColorSwatchItem.border_color_active

    def __init__(self):
        super().__init__()

        self.setPen(QPen(ColorSampleItem.border_color, ColorSampleItem.border_thickness))

class ColorSampleItem(QGraphicsEllipseItem):
    radius              = 40
    border_thickness    = 4
    border_color        = ColorSwatchItem.border_color_active
    items               = list()

    def __init__(self, project, position=QPointF()):
        super().__init__()
        
        ColorSampleItem.items.append(self)

        self.project                = project
        self.color_swatch_item      = None
        self.link_item              = LinkItem()
        self.anchor_position_scene  = QPointF()

        self.project.scene.addItem(self.link_item)

        self.setPen(QPen(QApplication.instance().palette().color(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text), ColorSampleItem.border_thickness))
        self.setRect(position.x() - ColorSampleItem.radius / 2, position.y() - ColorSampleItem.radius / 2, ColorSampleItem.radius, ColorSampleItem.radius)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        self.setRect(position.x() - ColorSampleItem.radius / 2, position.y() - ColorSampleItem.radius / 2, ColorSampleItem.radius, ColorSampleItem.radius)

        self.update()

    def __del__(self):
        """Remove item from tracking when deleted."""

        if self in ColorSampleItem.items:
            ColorSampleItem.items.remove(self)

    def update(self):
        """Update tge """

        sample_color = Qt.GlobalColor.black
        
        if self.project.reference_image:
            scene_pos           = self.mapToScene(self.rect().center())
            reference_position  = self.project.reference_item.mapFromScene(scene_pos)
            sample_color        = self.project.reference_image.pixelColor(reference_position.toPoint())
            
            # print("////", self.position)
            self.setBrush(QBrush(sample_color))

        self.connect_all_samples()

        if self.color_swatch_item:
            self.color_swatch_item.sample_color = sample_color
            self.color_swatch_item.update()

    def connect_all_samples(self):
        """Connect all color samples to a color swatches."""

        for color_swatch_item in ColorSwatchItem.items:
            color_swatch_item.disconnect_from_color_sample_item()

        for color_sample_item in ColorSampleItem.items:
            links = list()

            for color_swatch_item in [item for item in ColorSwatchItem.items if not item.color_sample_item]:
                # print(color_swatch_item.anchor_position_scene)
                links.append(Link(color_sample_item, color_swatch_item))

            if not links:
                continue

            links.sort(key=lambda item: item.distance)

            # for l in links:
            #     print(l.distance)

            color_sample_item.connect_to_color_swatch_item(links[0].color_swatch_item)

    def connect_to_color_swatch_item(self, color_swatch_item):
        """Connect to color swatch item."""

        self.color_swatch_item = color_swatch_item

        self.color_swatch_item.connect_to_color_sample_item(self)

        self.color_swatch_item.sample_color = self.brush().color()

        self.link_item.setLine(QLineF(self.anchor_position_scene, self.color_swatch_item.anchor_position_scene))

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemVisibleHasChanged:
            self.anchor_position_scene = self.mapToScene(self.rect().center())

            self.update()

        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionHasChanged:
            self.anchor_position_scene = self.mapToScene(self.rect().center())

            self.update()

        return super().itemChange(change, value)
   
    def to_dict(self):
        """Convert the color sample to a dictionary."""

        scene_pos   = self.mapToScene(self.rect().center())
        position    = scene_pos#self.project.reference_item.mapFromScene(scene_pos)

        return {
            "Position": {
                "X": position.x(),
                "Y": position.y()
            }
        }
    
    @staticmethod
    def from_dict(project, dict):
        """Create color sample item from dictionary."""

        return ColorSampleItem(project, QPointF(dict["Position"]["X"], dict["Position"]["Y"]))
        try:
            print(dict)
            return ColorSampleItem(project, QPointF(dict["Position"]["X"], dict["Position"]["Y"]))
        except Exception as e:
            print(f"Cannot initialize color sample from dictionary: {e}")