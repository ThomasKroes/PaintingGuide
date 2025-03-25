from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsView, QGraphicsScene, QFileDialog, QApplication
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject

import os, json, zipfile, tempfile, shutil

from project_widget import ProjectWidget
from project_view import ProjectView
from project import *

class Project(QObject):
    def __init__(self, reference_image_file_path=""):
        super().__init__()

        self.reference_image_file_path  = reference_image_file_path
        self.project_scene              = QGraphicsScene()
        self.project_view               = ProjectView(self.project_scene)
        self.project_widget             = ProjectWidget(reference_image_file_path)
        self.temp_dir_load              = tempfile.mkdtemp()
        self.temp_dir_save              = tempfile.mkdtemp()

        self.project_view.setScene(self.project_scene)
        self.project_scene.addWidget(self.project_widget)

    def load(self, project_file_path):
        """Load project from disk."""

        try:
            with zipfile.ZipFile(project_file_path, 'r') as zip_file:
                zip_file.extractall(self.temp_dir_load)
            
            self.from_json_file(os.path.join(self.temp_dir_load, "Project.json"))
            
            self.project_widget.set_reference_image_file_path(os.path.join(self.temp_dir_load, "Reference.jpg"))

            print(self.temp_dir_load)
            print(project_file_path)
            print(os.listdir(self.temp_dir_load))
        except FileNotFoundError:
            print(f"Error: The zip file { project_file_path } was not found.")
        except zipfile.BadZipFile:
            print(f"Error: The file { project_file_path } is not a valid zip file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def save(self):
        """Save project to disk."""

        last_project_dir = QApplication.instance().settings.value("Directories/ProjectDir")

        project_file_path, _ = QFileDialog.getSaveFileName(None, "Save project", last_project_dir, "Painting Guide Project (*.pgp)")

        shutil.copy(self.reference_image_file_path, os.path.join(self.temp_dir_save, "Reference.jpg"))

        self.save_to_temp_file()

        zip_input_file_paths = ["Reference.jpg", "Project.json"]

        if project_file_path:
            with zipfile.ZipFile(project_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for zip_input_file_name in zip_input_file_paths:
                    zip_file.write(os.path.join(self.temp_dir_save, zip_input_file_name), arcname=os.path.basename(zip_input_file_name))

            QApplication.instance().settings.setValue("Directories/ProjectDir", os.path.dirname(project_file_path))

    def to_dict(self):
        """Convert the project properties to a dictionary."""

        return {
            "ReferenceImageFilePath": self.reference_image_file_path
        }

    def from_json(self, json):
        """Serialize the project from JSON."""

        self.reference_image_file_path = json["ReferenceImageFilePath"]
    
    def to_json(self):
        """Serialize the project to JSON."""
        
        return json.dumps(self.to_dict(), indent=4)
    
    def from_json_file(self, project_json_file_path):
        """Load project from JSON file."""

        with open(project_json_file_path, 'r') as project_json_file:
            json_data = json.load(project_json_file)

        self.from_json(json_data)
    
    def save_to_temp_file(self, filename="Project.json"):
        """Save JSON to a temporary directory with a custom filename."""
        
        temp_file_path = os.path.join(self.temp_dir_save, filename)
        
        with open(temp_file_path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4)
        
        return temp_file_path