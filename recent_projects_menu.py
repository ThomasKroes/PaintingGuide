from PyQt6.QtWidgets import QMenu, QApplication
from PyQt6.QtGui import QAction

import qtawesome as qta

from color_sample_item import ColorSampleItem

class RecentProjectsMenu(QMenu):
    def __init__(self, parent):
        super().__init__("Recent projects", parent)
        
        self.setIcon(qta.icon("fa5s.clock"))

        self.populate()

    def get_recent_projects(self):
        """Get recent projects from application settings."""

        return QApplication.instance().settings.value("Projects/Recent", [], type=list)

    def showEvent(self, a0):
        """Invoked when the menu is shown."""

        super().showEvent(a0)
    
    def populate(self):
        self.clear()

        recent_projects = self.get_recent_projects()

        for recent_project in recent_projects:
            open_recent_project_action = QAction(recent_project, self)

            open_recent_project_action.setIcon(qta.icon("fa5s.image"))
            open_recent_project_action.setShortcut(f"Alt+{ recent_projects.index(recent_project) + 1 }")

            open_recent_project_action.triggered.connect(lambda checked=False, p=recent_project: self.open_recent_project(p))
            
            self.addAction(open_recent_project_action)

        if not self.actions():
            self.setEnabled(False)

    def open_recent_project(self, file_path):
        """Open recent project from disk."""

        self.parent().open_project(file_path)
    