from PyQt6.QtWidgets import QLabel, QMessageBox, QGraphicsView, QGraphicsScene, QFileDialog, QApplication, QGraphicsGridLayout, QGraphicsLayoutItem, QGraphicsWidget
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath, QPixmap, QImage
from PyQt6.QtCore import Qt, QRectF, QMarginsF, QObject, QPoint, QPointF, QSizeF

import os, json, zipfile, tempfile, shutil, traceback

from project_view import ProjectView
from reference_item import ReferenceItem
from color_swatches import ColorSwatches
from color_swatch_item import ColorSwatchItem
from color_samples import ColorSamples
from color_sample_item import ColorSampleItem
from color_sample_links import ColorSampleLinks

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
        self.color_swatches             = ColorSwatches(self)
        self.color_samples              = ColorSamples(self)
        self.color_sample_links         = ColorSampleLinks(self)
        self.file_path                  = ""
        self.export_image_file_path     = ""
        self.color_dialog               = None

        self.scene.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)
        
        self.view.setScene(self.scene)

        self.scene.addItem(self.reference_item)
        
        self.load_reference_image(reference_image_file_path)
        
        self.color_swatches.update()

    def load_reference_image(self, reference_image_file_path):
        """ ."""

        if not os.path.exists(reference_image_file_path):
            return

        self.reference_image_file_path = reference_image_file_path

        self.reference_image = QPixmap(reference_image_file_path).toImage()

        if self.reference_image.isNull():
            raise RuntimeError("Reference image not valid")

        reference_image_size = self.reference_image.size()

        self.reference_item.set_fixed_size(reference_image_size.toSizeF())

        swatches_size = 4 * ColorSwatchItem.swatch_spacing + 2 * ColorSwatchItem.swatch_size 

        self.root_widget.resize(reference_image_size.toSizeF() + QSizeF(swatches_size, swatches_size))

    def open(self, file_path):
        """Open project from disk."""

        try:
            print(f"Open project from: { file_path }")

            with zipfile.ZipFile(file_path, 'r') as zip_file:
                zip_file.extractall(self.temp_dir_load)
            
            self.from_json_file(os.path.join(self.temp_dir_load, "Project.json"))

            reference_image_file_path = os.path.join(self.temp_dir_load, "Reference.jpg")

            self.load_reference_image(reference_image_file_path)

            self.file_path = file_path

            app_settings = QApplication.instance().settings

            recent_projects = app_settings.value("Projects/Recent", [], type=list)

            recent_projects.append(self.file_path)

            app_settings.setValue("Projects/Recent", list(dict.fromkeys(recent_projects)))
        except FileNotFoundError:
            print(f"Error: The zip file { file_path } was not found.")
        except zipfile.BadZipFile:
            print(f"Error: The file { file_path } is not a valid zip file.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def save(self, file_path="", choose_location=False):
        """Save to disk (ask for location if file_path is empty)."""

        if choose_location or not self.file_path:
            last_project_dir = QApplication.instance().settings.value("Directories/ProjectDir")

            self.file_path, _ = QFileDialog.getSaveFileName(None, "Save project", last_project_dir, "Painting Guide Project (*.pgp)")

        print(f"Save project to: { self.file_path }")

        shutil.copy(self.reference_image_file_path, os.path.join(self.temp_dir_save, "Reference.jpg"))

        self.save_to_temp_file()

        zip_input_file_paths = ["Reference.jpg", "Project.json"]

        app_settings = QApplication.instance().settings

        if self.file_path:
            with zipfile.ZipFile(self.file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for zip_input_file_name in zip_input_file_paths:
                    zip_file.write(os.path.join(self.temp_dir_save, zip_input_file_name), arcname=os.path.basename(zip_input_file_name))

            app_settings.setValue("Directories/ProjectDir", os.path.dirname(self.file_path))

    def save_as(self):
        """Save to disk in a picked location."""

        self.save("", True)

    def export_to_image(self, file_path="", choose_location=False):
        """Export to image (ask for location if file_path is empty)."""

        if choose_location or not self.export_image_file_path:
            last_export_dir = QApplication.instance().settings.value("Directories/Export")

            self.export_image_file_path, _ = QFileDialog.getSaveFileName(None, "Export to image", last_export_dir, "Image (*.png)")

        print(f"Export image to: { self.export_image_file_path }")

        if self.export_image_file_path:
            scene_rect = self.scene.itemsBoundingRect()

            image = QImage(scene_rect.size().toSize(), QImage.Format.Format_ARGB32)
            image.fill(self.view.backgroundBrush().color()) 

            painter = QPainter(image)
            self.scene.render(painter, target=scene_rect)
            painter.end()

            image.save(self.export_image_file_path)

            QApplication.instance().settings.setValue("Directories/Export", os.path.dirname(self.export_image_file_path))

    def export_to_image_as(self):
        """Export to image in a picked location."""

        self.export_to_image("", True)

    def save_to_dict(self, dict : dict):
        """Save in dictionary."""

        try:
            dict["ReferenceImageFilePath"] = self.reference_image_file_path

            self.color_swatches.save_to_dict(dict)
            self.color_samples.save_to_dict(dict)
            self.color_sample_links.save_to_dict(dict)
        except Exception as e:
            print(f"Cannot save project to dictionary: {e}")
            traceback.print_exc()
        
    def load_from_dict(self, dict : dict):
        """Load from dictionary."""

        try:
            self.load_reference_image(dict["ReferenceImageFilePath"])

            self.color_swatches.load_from_dict(dict)
            self.color_samples.load_from_dict(dict)
            self.color_sample_links.load_from_dict(dict)

            self.color_sample_links.choose_links(True)
        except Exception as e:
            print(f"Cannot load project from dictionary: {e}")
            traceback.print_exc()

    def to_json(self):
        """Serialize the project to JSON."""
        
        return json.dumps(self.to_dict(), indent=4)
    
    def from_json_file(self, project_json_file_path):
        """Load project from JSON file."""

        with open(project_json_file_path, 'r') as project_json_file:
            json_data = json.load(project_json_file)

        self.load_from_dict(json_data)
    
    def save_to_temp_file(self, filename="Project.json"):
        """Save JSON to a temporary directory with a custom filename."""
        
        temp_file_path = os.path.join(self.temp_dir_save, filename)
        
        project = dict()

        self.save_to_dict(project)

        with open(temp_file_path, "w", encoding="utf-8") as file:
            json.dump(project, file, indent=4)
        
        return temp_file_path