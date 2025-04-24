# curling_league_manager/gui/member_editor.py
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox
)
from curling_league_manager.core.models import Member

class MemberEditorDialog(QDialog):
    def __init__(self, member=None, parent=None):
        super().__init__(parent)
        # If editing an existing member, we receive it; otherwise create a blank one
        self.member = member or Member(name="", email="")
        self.setWindowTitle("Edit Member" if member else "Add Member")
        self._setup_ui()

    def _setup_ui(self):
        layout = QFormLayout()
        self.name_edit  = QLineEdit(self.member.name)
        self.email_edit = QLineEdit(self.member.email)
        layout.addRow("Name:",  self.name_edit)
        layout.addRow("Email:", self.email_edit)

        btn_save   = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(self._save)
        btn_cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)

        self.setLayout(layout)

    def _save(self):
        name  = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "Invalid", "Both name and email are required.")
            return
        self.member.name  = name
        self.member.email = email
        self.accept()
