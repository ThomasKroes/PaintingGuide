from PyQt6.QtWidgets import QWidget

class MainToolbarWidget(QWidget):
    def __init__(self, project):
        super().__init__()

        self.project = project