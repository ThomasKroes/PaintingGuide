import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QFileDialog, QMessageBox, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QAction, QPixmap, QColor
from PyQt6.QtCore import Qt, QSettings, QSize

from color_swatch import ColorSwatch

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Kroes", "Paint guide")  # Store settings

        self.setWindowTitle("Painting guide")

        # Restore window position and size
        self.resize(self.settings.value("window/size", QSize(800, 600)))
        self.move(self.settings.value("window/position", self.pos()))

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set up QGridLayout with extra padding
        grid_layout = QGridLayout(central_widget)

        grid_layout.setContentsMargins(10, 10, 10, 10)  # Extra space around the whole layout
        grid_layout.setSpacing(0)  # Optional: Adjust spacing between elements

        # QLabel to display the image
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(False)  # Prevent QLabel from stretching
        
        grid_layout.addWidget(self.label, 1, 1)  # Center position for the pixmap

        self.top_layout     = QHBoxLayout()
        self.bottom_layout  = QHBoxLayout()
        self.left_layout    = QVBoxLayout()
        self.right_layout   = QVBoxLayout()

        self.border_layouts = [self.top_layout, self.bottom_layout, self.left_layout, self.right_layout]
        
        grid_layout.addLayout(self.top_layout, 0, 1)
        grid_layout.addLayout(self.bottom_layout, 2, 1)
        grid_layout.addLayout(self.left_layout, 1, 0)
        grid_layout.addLayout(self.right_layout, 1, 2)

        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(2, 1)

        for border_layout in self.border_layouts:
            border_layout.setSpacing(ColorSwatch.spacing)
            border_layout.setContentsMargins(ColorSwatch.margin, ColorSwatch.margin, ColorSwatch.margin, ColorSwatch.margin)

        grid_layout.setAlignment(self.left_layout, Qt.AlignmentFlag.AlignTop)

        self.pixmap = None  # Store the original pixmap
        self.last_dir = self.settings.value("last_dir", os.path.expanduser("~"))  # Restore last directory
        
        self.create_menu_bar()
        

    def populate_color_swatches_layout(self, layout, num_color_swatches, alignment):
        """Populate left, right top or bottom layout with color swatches"""

        layout.addStretch(1)

        for i in range(num_color_swatches):
            color_swatch = ColorSwatch()

            layout.addWidget(color_swatch)
            layout.setAlignment(color_swatch, alignment)

        layout.addStretch(1)

    def add_color_swatches(self, layout):
        """ Add color swatches around the reference image"""

        if self.pixmap:
            img_width   = self.pixmap.width()
            img_height  = self.pixmap.height()
            size        = ColorSwatch.size + ColorSwatch.spacing

            num_top_bottom = (img_width // size)
            num_left_right = (img_height // size)

            self.populate_color_swatches_layout(self.top_layout, num_top_bottom, Qt.AlignmentFlag.AlignBottom)
            self.populate_color_swatches_layout(self.bottom_layout, num_top_bottom, Qt.AlignmentFlag.AlignTop)
            self.populate_color_swatches_layout(self.left_layout, num_left_right, Qt.AlignmentFlag.AlignRight)
            self.populate_color_swatches_layout(self.right_layout, num_left_right, Qt.AlignmentFlag.AlignLeft)

    def create_menu_bar(self):
        # Create menu bar
        menu_bar = self.menuBar()

        # Add "File" menu
        file_menu = menu_bar.addMenu("File")

        # Add "Open" action
        open_action = QAction("Open JPG", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Add "Exit" action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", self.last_dir, "Images (*.jpg *.jpeg *.png *.bmp)"
        )

        if file_path:
            self.last_dir = os.path.dirname(file_path)  # Store the last opened directory
            self.settings.setValue("last_dir", self.last_dir)  # Save it to settings

            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.warning(self, "Error", "Failed to load image!")
            else:
                self.pixmap = pixmap  # Store original image
                self.update_scaled_pixmap()
                self.add_color_swatches(self.centralWidget().layout())  # Add swatches after loading image

    def resizeEvent(self, event):
        """ Resize image while keeping the aspect ratio when the window is resized """
        self.update_scaled_pixmap()
        self.settings.setValue("window/size", self.size())  # Save size to settings
        super().resizeEvent(event)

    def moveEvent(self, event):
        """ Save window position when moved """
        self.settings.setValue("window/position", self.pos())  # Save position to settings
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
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
