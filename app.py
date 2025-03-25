import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QTabWidget 
from PyQt6.QtGui import QAction, QPixmap, QColor
from PyQt6.QtCore import Qt, QSettings, QSize

from color_swatch import ColorSwatch
from project import Project

class PaintingGuide(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Kroes", "Paint guide")

        self.setWindowTitle("Painting guide")
        self.resize(self.settings.value("window/size", QSize(800, 600)))
        self.move(self.settings.value("window/position", self.pos()))
        
        self.tab_widget = QTabWidget()

        self.setCentralWidget(self.tab_widget)

        self.pixmap     = None
        self.last_dir   = self.settings.value("last_dir", os.path.expanduser("~"))
        self.projects   = []

        self.create_menu_bar()   
        self.update_save_project_action_read_only()

        self.tab_widget.currentChanged.connect(self.update_save_project_action_read_only)

    def create_menu_bar(self):
        """Creates the main menu bar"""

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        
        self.import_reference_image_action = QAction("Import reference image", self)
        self.import_reference_image_action.triggered.connect(self.import_reference_image)

        file_menu.addAction(self.import_reference_image_action)

        file_menu.addSeparator()

        self.open_project_action = QAction("Open project", self)
        self.open_project_action.triggered.connect(self.open_project)

        file_menu.addAction(self.open_project_action)

        self.save_project_action = QAction("Save project", self)
        self.save_project_action.triggered.connect(self.save_project)

        file_menu.addAction(self.save_project_action)

        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)
        
        file_menu.addAction(self.exit_action)

    def import_reference_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", self.last_dir, "Images (*.jpg *.jpeg *.png *.bmp)")

        if file_path:
            self.last_dir = os.path.dirname(file_path)
            self.settings.setValue("Directories/ReferenceImageDir", self.last_dir)

            self.create_project(file_path)

    def create_project(self, reference_image_file_path):
        """Create project from reference image file path."""

        project = Project(reference_image_file_path)

        self.tab_widget.addTab(project.project_view, os.path.basename(reference_image_file_path))
        
    def open_project(self):
        pass

    def save_project(self):
        """Saves the current project to disk"""

        if self.tab_widget.currentIndex() < 0:
            return

        self.tab_widget.currentWidget().super().save()

    def update_save_project_action_read_only(self):
        """Updates the read-only state of the save project action"""

        self.save_project_action.setEnabled(self.tab_widget.currentIndex() >= 0)
    
    def resizeEvent(self, event):
        """ Resize image while keeping the aspect ratio when the window is resized."""

        self.settings.setValue("window/size", self.size())
        
        super().resizeEvent(event)

    def moveEvent(self, event):
        """ Save window position when moved."""

        self.settings.setValue("window/position", self.pos())

        super().moveEvent(event)

    def update_scaled_pixmap(self):
        """ Update QLabel with a scaled pixmap while maintaining aspect ratio """
        if self.pixmap:
            window_size = self.centralWidget().size()

            # Scale pixmap while maintaining aspect ratio
            scaled_pixmap = self.pixmap.scaled(
                window_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)

            # Ensure QLabel resizes properly
            self.label.setMinimumSize(1, 1)  # Allow shrinking

if __name__ == "__main__":
    app     = QApplication(sys.argv)
    window  = PaintingGuide()

    window.show()
    
    sys.exit(app.exec())
