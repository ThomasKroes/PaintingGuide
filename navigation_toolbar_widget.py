from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QDoubleSpinBox, QSlider
from PyQt6.QtCore import Qt, QSize

import qtawesome as qta

class NavigationToolbarWidget(QWidget):
    def __init__(self, project):
        super().__init__()

        self.project                    = project
        self.layout                     = QHBoxLayout()
        self.zoom_out_push_button       = QPushButton()
        self.zoom_percentage_spinbox    = QDoubleSpinBox()
        self.zoom_percentage_slider     = QSlider(Qt.Orientation.Horizontal)
        self.zoom_in_push_button        = QPushButton()
        self.zoom_extents_push_button   = QPushButton()
        
        self.zoom_out_push_button.setToolTip("Zoom out by 10%")
        self.zoom_percentage_spinbox.setToolTip("Set the zoom percentage")
        self.zoom_percentage_slider.setToolTip("Set the zoom percentage")
        self.zoom_in_push_button.setToolTip("Zoom in by 10%")
        self.zoom_extents_push_button.setToolTip("Zoom to the extents")

        self.zoom_out_push_button.setIconSize(QSize(12, 12))
        self.zoom_in_push_button.setIconSize(QSize(12, 12))
        self.zoom_extents_push_button.setIconSize(QSize(12, 12))

        self.zoom_out_push_button.setIcon(qta.icon("fa5s.search-minus"))
        self.zoom_in_push_button.setIcon(qta.icon("fa5s.search-plus"))
        self.zoom_extents_push_button.setIcon(qta.icon("fa5s.compress"))

        self.zoom_percentage_spinbox.setFixedWidth(120)
        self.zoom_percentage_spinbox.setSuffix(" %")
        self.zoom_percentage_spinbox.setDecimals(1)

        self.zoom_percentage_slider.setFixedWidth(250)

        self.layout.setContentsMargins(2, 2, 2, 2)

        self.layout.addStretch(1)
        
        self.layout.addWidget(self.zoom_out_push_button)
        self.layout.addWidget(self.zoom_percentage_spinbox)
        self.layout.addWidget(self.zoom_percentage_slider)
        self.layout.addWidget(self.zoom_in_push_button)
        self.layout.addWidget(self.zoom_extents_push_button)

        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.zoom_out_push_button.clicked.connect(self.project.view.zoom_out)
        self.zoom_in_push_button.clicked.connect(self.project.view.zoom_in)
        self.zoom_extents_push_button.clicked.connect(self.project.view.zoom_extents)

        self.project.view.zoom_factor_changed.connect(self.on_zoom_factor_changed)

    def on_zoom_factor_changed(self, zoom_factor : float):
        """Invoked when the project view zoom factor changes."""

        self.zoom_percentage_spinbox.setValue(zoom_factor)
        self.zoom_percentage_spinbox.setValue(zoom_factor * 10000)