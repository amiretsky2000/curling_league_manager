# curling_league_manager/gui/team_editor.py
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QMessageBox

class TeamEditorDialog(QDialog):
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.team = team
        self.setWindowTitle(f"Edit Team: {team.name}")
        self._setup_ui()

    def _setup_ui(self):
        layout = QFormLayout()
        self.name_edit  = QLineEdit(self.team.name)
        layout.addRow("Team Name:", self.name_edit)

        # Member list + controls could go here if desired...
        # For simplicity, this dialog only renames the team.
        
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self._save)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def _save(self):
        new_name = self.name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Invalid", "Name cannot be blank.")
            return
        self.team.name = new_name
        self.accept()
