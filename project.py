from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsView, QGraphicsScene, QFileDialog
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject

import os, json

from project_widget import ProjectWidget
from project_view import ProjectView

class Project(QObject):
    def __init__(self, reference_image_file_path):
        super().__init__()

        self.project_scene  = QGraphicsScene()
        self.project_view   = ProjectView(self.project_scene)
        self.project_widget = ProjectWidget(reference_image_file_path)
        
        self.project_view.setScene(self.project_scene)

        self.project_scene.addWidget(self.project_widget)

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save project", self.last_dir, "Painting guide project (*.pgp)")

        if file_path:
            self.last_dir = os.path.dirname(file_path)
            
            self.settings.setValue("Directories/ProjectDir", self.last_dir)

    def to_dict(self):
        """Convert the project properties to a dictionary."""

        return {
            "name": self.name,
            "age": self.age
        }

    def to_json(self):
        """Serialize the project to JSON."""

        return json.dumps(self.to_dict(), indent=4)