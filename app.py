import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox, QGridLayout, QHBoxLayout, QMenu, QWidget, QSpacerItem, QSizePolicy, QTabWidget, QToolBar
from PyQt6.QtGui import QAction, QPixmap, QColor
from PyQt6.QtCore import Qt, QSettings, QSize

import qtawesome as qta

from color_swatch_item import ColorSwatchItem
from project import Project
from recent_projects_menu import RecentProjectsMenu

class PaintingGuide(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Painting guide")
        self.resize(app.settings.value("Window/Size", QSize(800, 600)))
        self.move(app.settings.value("Window/Position", self.pos()))
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tab_widget)

        self.pixmap             = None
        self.projects           = []
        
        app.opening_project    = False
        app.saving_project     = False

        self.create_menu_bar()   
        self.update_actions_read_only()

        self.tab_widget.currentChanged.connect(self.update_actions_read_only)

    def create_menu_bar(self):
        """Creates the main menu bar."""

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        
        self.import_reference_image_action = QAction("Import reference image", self)
        self.import_reference_image_action.triggered.connect(self.import_reference_image)
        self.import_reference_image_action.setIcon(qta.icon("fa5s.file-import"))

        file_menu.addAction(self.import_reference_image_action)

        file_menu.addSeparator()

        self.open_project_action = QAction("Open project", self)
        self.open_project_action.setIcon(qta.icon("fa5s.folder-open"))
        self.open_project_action.triggered.connect(self.open_project)

        file_menu.addAction(self.open_project_action)

        self.save_project_action = QAction("Save project", self)
        self.save_project_action.setIcon(qta.icon("fa5s.save"))
        self.save_project_action.triggered.connect(self.save_project)

        file_menu.addAction(self.save_project_action)

        self.save_project_as_action = QAction("Save project as...", self)
        self.save_project_as_action.setIcon(qta.icon("fa5s.save"))
        self.save_project_as_action.triggered.connect(self.save_project_as)

        file_menu.addAction(self.save_project_as_action)

        file_menu.addSeparator()

        self.export_project_to_image_action = QAction("Export project", self)
        self.export_project_to_image_action.setIcon(qta.icon("fa5s.file-export"))
        self.export_project_to_image_action.triggered.connect(self.export_project_to_image)

        file_menu.addAction(self.export_project_to_image_action)

        self.export_project_to_image_as_action = QAction("Export project as...", self)
        self.export_project_to_image_as_action.setIcon(qta.icon("fa5s.file-export"))
        self.export_project_to_image_as_action.triggered.connect(self.export_project_to_image_as)

        file_menu.addAction(self.export_project_to_image_as_action)

        file_menu.addSeparator()
        
        file_menu.addMenu(RecentProjectsMenu(self))

        file_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.setIcon(qta.icon("fa5s.sign-out-alt"))
        self.exit_action.triggered.connect(self.close)

        file_menu.addAction(self.exit_action)

        self.toolbar = QToolBar("Tools")

        # self.addToolBar(self.toolbar)

        # # Add color picker action
        # color_action = QAction(QIcon(), "Pick Color", self)
        # color_action.triggered.connect(self.pick_color)
        # self.toolbar.addAction(color_action)

    def import_reference_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", app.settings.value("Directories/ReferenceImageDir", os.path.expanduser("~")), "Images (*.jpg *.jpeg *.png *.bmp)")

        if file_path:
            self.last_dir = os.path.dirname(file_path)
            app.settings.setValue("Directories/ReferenceImageDir", self.last_dir)

            self.create_project(file_path)

    def create_project(self, reference_image_file_path):
        """Create project from reference image file path."""

        self.projects.append(Project(reference_image_file_path))

        self.tab_widget.addTab(self.projects[-1].view, os.path.basename(reference_image_file_path))

    def open_project(self, file_path):
        """Open a project from disk."""

        self.begin_open_project()
        
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Project", app.settings.value("Directories/ProjectDir", os.path.expanduser("~")), "Painting Guide Project (*.pgp)")

        app.settings.setValue("Directories/ProjectDir", os.path.dirname(file_path))

        project = Project()

        self.projects.append(project)

        project.open(file_path)

        self.tab_widget.addTab(project.view, os.path.basename(project.reference_image_file_path))

        self.end_open_project()

    def save_project(self):
        """Saves the current project to disk."""

        self.begin_save_project()

        if self.tab_widget.currentIndex() >= 0:
            self.projects[self.tab_widget.currentIndex()].save()

        self.end_save_project()

    def save_project_as(self):
        """Saves the current project to disk in a picked location."""

        if self.tab_widget.currentIndex() >= 0:
            self.projects[self.tab_widget.currentIndex()].save_as()

    def export_project_to_image(self):
        """Exports the current project to an image file."""

        if self.tab_widget.currentIndex() >= 0:
            self.projects[self.tab_widget.currentIndex()].export_to_image()

    def export_project_to_image_as(self):
        """Exports the current project to an image file in a picked location."""

        if self.tab_widget.currentIndex() >= 0:
            self.projects[self.tab_widget.currentIndex()].export_to_image_as()

    def begin_open_project(self):
        """Begin opening a project """

        print("Begin open project")
        self.opening_project = True

    def end_open_project(self):
        """End opening a project """

        print("End open project")
        self.opening_project = False

    def begin_save_project(self):
        """Begin saving a project """

        print("Begin save project")
        self.saving_project = True

    def end_save_project(self):
        """End saving a project """

        print("End save project")
        self.saving_project = False

    def update_actions_read_only(self):
        """Updates the read-only state of various actions."""

        self.save_project_action.setEnabled(self.tab_widget.currentIndex() >= 0)
        self.save_project_as_action.setEnabled(self.tab_widget.currentIndex() >= 0)
        self.export_project_to_image_action.setEnabled(self.tab_widget.currentIndex() >= 0)
        self.export_project_to_image_as_action.setEnabled(self.tab_widget.currentIndex() >= 0)
    
    def close_tab(self, index):
        """Remove tab when close button is clicked."""
        
        self.tab_widget.removeTab(index)

        self.projects.pop(index)

    def resizeEvent(self, event):
        """ Resize image while keeping the aspect ratio when the window is resized."""

        app.settings.setValue("Window/Size", self.size())
        
        super().resizeEvent(event)

    def moveEvent(self, event):
        """ Save window position when moved."""

        app.settings.setValue("Window/Position", self.pos())

        super().moveEvent(event)

    def update_scaled_pixmap(self):
        """ Update QLabel with a scaled pixmap while maintaining aspect ratio """
        if self.pixmap:
            window_size = self.centralWidget().size()

            scaled_pixmap = self.pixmap.scaled(window_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            self.label.setPixmap(scaled_pixmap)

            self.label.setMinimumSize(1, 1)  # Allow shrinking

if __name__ == "__main__":
    app     = QApplication(sys.argv)

    app.setWindowIcon((qta.icon("fa5s.palette")))
    app.settings = QSettings("Kroes", "Paint guide")

    window  = PaintingGuide()

    window.show()
    
    sys.exit(app.exec())
