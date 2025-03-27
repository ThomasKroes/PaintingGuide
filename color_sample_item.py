from PyQt6.QtWidgets import QLabel, QGraphicsEllipseItem, QGraphicsItem
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QSizeF, QPointF

from color_swatch import ColorSwatch

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class ColorSampleItem(QGraphicsEllipseItem):
    radius              = 50
    border_thickness    = 5
    border_color        = ColorSwatch.border_color_active

    def __init__(self, project, color=QColor(), position=QPointF()):
        super().__init__()
        
        self.project    = project
        self.color      = color
        self.position   = position

        self.setBrush(QBrush())
        self.setPen(QPen(ColorSampleItem.border_color, ColorSampleItem.border_thickness))
        # self.setPos(position.toPointF())
        self.setRect(position.x(), position.y(), ColorSampleItem.radius, ColorSampleItem.radius)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
    
        self.update()

        print(position)
    
    def update(self):
        """"""

        scene_pos       = self.mapToScene(self.rect().center())
        reference_pos   = self.project.reference_item.mapFromScene(scene_pos)
        pixel_color     = self.project.reference_image.pixelColor(reference_pos.toPoint())
        
        self.setBrush(QBrush(pixel_color))

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.GraphicsItemChange.ItemPositionChange:
            self.update()
            # new_pos = value  # Proposed new position

            # # Map the new position to the proxy widget's local coordinates
            # local_pos = self.project.widget_proxy.mapFromScene(new_pos)

            # # Get the bounding rect of the widget inside the QGraphicsProxyWidget
            # widget_rect = self.project.widget.reference_label.geometry()

            # # Clamp the x and y position within the widget's rect
            # x = min(max(local_pos.x(), 0), widget_rect.width() - self.rect().width())
            # y = min(max(local_pos.y(), 0), widget_rect.height() - self.rect().height())

            # # Map the clamped position back to the scene coordinates
            # return self.project.widget_proxy.mapToScene(QPointF(x, y))

        return super().itemChange(change, value)
   
    def to_dict(self):
        """Convert the color sample to a dictionary."""

        return {
            "Color": {
                "Red": self.color.red(),
                "Green": self.color.green(),
                "Blue": self.color.blue(),
            },
            "Position": {
                "X": self.position.x(),
                "Y": self.position.y()
            }
        }
    
    @staticmethod
    def from_dict(project, dict):
        """Create color sample item from dictionary."""

        try:
            color_sample = ColorSampleItem(project)

            color_sample.color.setRed(dict["Color"]["Red"])
            color_sample.color.setGreen(dict["Color"]["Green"])
            color_sample.color.setBlue(dict["Color"]["Blue"])
            
            color_sample.position.setX(dict["Position"]["X"])
            color_sample.position.setY(dict["Position"]["Y"])

            return color_sample
        except Exception as e:
            print(f"Cannot initialize color sample from dictionary: {e}")