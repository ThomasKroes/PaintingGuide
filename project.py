from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsView, QGraphicsScene, QFileDialog, QApplication, QGraphicsGridLayout, QGraphicsLayoutItem, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QPointF, QSizeF

import os, json, zipfile, tempfile, shutil

from project_widget import ProjectWidget
from project_view import ProjectView
from reference_item import ReferenceItem
from color_sample_item import ColorSampleItem
from color_swatches import ColorSwatches
from color_swatch import ColorSwatch

class Project(QObject):
    def __init__(self, reference_image_file_path=""):
        super().__init__()

        self.reference_image            = None
        self.reference_image_file_path  = ""
        self.scene                      = QGraphicsScene()
        self.view                       = ProjectView(self)
        self.temp_dir_load              = tempfile.mkdtemp()
        self.temp_dir_save              = tempfile.mkdtemp()
        self.root_widget                = QGraphicsWidget()
        self.grid_layout                = QGraphicsGridLayout()
        self.reference_item             = ReferenceItem(self)
        self.color_sample_items         = list()
        self.color_swatches             = ColorSwatches(self)

        self.grid_layout.setSpacing(0)
        self.grid_layout.addItem(self.reference_item, 1, 1)
        self.root_widget.setLayout(self.grid_layout)

        self.scene.addItem(self.root_widget)

        self.view.setScene(self.scene)
        
        self.load_reference_image(reference_image_file_path)

    def load_reference_image(self, reference_image_file_path):
        """ ."""

        if not os.path.exists(reference_image_file_path):
            return

        self.reference_image_file_path = reference_image_file_path

        self.reference_image = QPixmap(reference_image_file_path).toImage()

        if self.reference_image.isNull():
            raise RuntimeError("Reference image not valid")

        reference_image_size = self.reference_image.size()

        self.reference_item.resize(reference_image_size.width(), reference_image_size.height())

        swatches_size = 4 * ColorSwatch.swatch_spacing + 2 * ColorSwatch.swatch_size 

        self.root_widget.resize(reference_image_size.toSizeF() + QSizeF(swatches_size, swatches_size))

        self.color_swatches.update()

    def load(self, project_file_path):
        """Load project from disk."""

        try:
            with zipfile.ZipFile(project_file_path, 'r') as zip_file:
                zip_file.extractall(self.temp_dir_load)
            
            self.from_json_file(os.path.join(self.temp_dir_load, "Project.json"))

            reference_image_file_path = os.path.join(self.temp_dir_load, "Reference.jpg")

            self.load_reference_image(reference_image_file_path)

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

    def add_color_sample_from_scene_position(self, scene_position : QPoint):
        """Add color sample to the project."""
        
        if not self.reference_image:
            return
        
        reference_position  = self.reference_item.mapFromScene(scene_position.toPointF()).toPoint()
        color_sample_item   = ColorSampleItem(self, self.reference_image.pixelColor(reference_position), reference_position)
        
        self.add_color_sample(color_sample_item)

    def add_color_sample(self, color_sample_item : ColorSampleItem):
        """Add color sample to the project."""
        
        self.color_sample_items.append(color_sample_item)
        self.scene.addItem(color_sample_item)

        self.view.update()

    def to_dict(self):
        """Convert the project properties to a dictionary."""

        color_samples = list()

        for color_sample in self.color_sample_items:
            color_samples.append(color_sample.to_dict())

        print(color_samples)

        return {
            "ReferenceImageFilePath": self.reference_image_file_path,
            "ColorSamples": color_samples
        }

    def from_dict(self, dict):
        """Serialize the project from JSON."""

        self.reference_image_file_path = dict["ReferenceImageFilePath"]

        try:
            for color_sample_dict in dict["ColorSamples"]:
                self.add_color_sample(ColorSampleItem.from_dict(self, color_sample_dict))

        except Exception as e:
            print(f"Cannot load color samples from dictionary: {e}")
    
    def to_json(self):
        """Serialize the project to JSON."""
        
        return json.dumps(self.to_dict(), indent=4)
    
    def from_json_file(self, project_json_file_path):
        """Load project from JSON file."""

        with open(project_json_file_path, 'r') as project_json_file:
            json_data = json.load(project_json_file)

        self.from_dict(json_data)
    
    def save_to_temp_file(self, filename="Project.json"):
        """Save JSON to a temporary directory with a custom filename."""
        
        temp_file_path = os.path.join(self.temp_dir_save, filename)
        
        with open(temp_file_path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4)
        
        return temp_file_path