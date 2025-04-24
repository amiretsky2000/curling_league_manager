# curling_league_manager/gui/team_editor.py
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QListWidget, QInputDialog, QMessageBox
)
from curling_league_manager.core.models import Member

class TeamEditorDialog(QDialog):
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.team = team
        self.setWindowTitle(f"Edit Team: {team.name}")
        self._setup_ui()
        self._refresh_members()

    def _setup_ui(self):
        main_layout = QVBoxLayout()

        # Team name field
        form_layout = QFormLayout()
        self.name_edit = QLineEdit(self.team.name)
        form_layout.addRow("Team Name:", self.name_edit)
        main_layout.addLayout(form_layout)

        # Member list
        self.member_list = QListWidget()
        main_layout.addWidget(self.member_list)

        # Member buttons
        member_btns = QHBoxLayout()
        add_m = QPushButton("Add Member");    add_m.clicked.connect(self._add_member)
        edit_m = QPushButton("Edit Member");  edit_m.clicked.connect(self._edit_member)
        del_m = QPushButton("Delete Member"); del_m.clicked.connect(self._delete_member)
        for btn in (add_m, edit_m, del_m):
            member_btns.addWidget(btn)
        main_layout.addLayout(member_btns)

        # Save / Cancel
        action_btns = QHBoxLayout()
        save_btn = QPushButton("Save");   save_btn.clicked.connect(self._save)
        cancel = QPushButton("Cancel");   cancel.clicked.connect(self.reject)
        action_btns.addWidget(save_btn)
        action_btns.addWidget(cancel)
        main_layout.addLayout(action_btns)

        self.setLayout(main_layout)

    def _refresh_members(self):
        self.member_list.clear()
        for m in self.team.members:
            self.member_list.addItem(f"{m.name} <{m.email}> [{m.id[:6]}]")

    def _add_member(self):
        name, ok = QInputDialog.getText(self, "Add Member", "Member name:")
        if not ok or not name.strip(): return
        email, ok = QInputDialog.getText(self, "Add Member", "Member email:")
        if not ok or not email.strip(): return

        self.team.members.append(Member(name=name.strip(), email=email.strip()))
        self._refresh_members()

    def _edit_member(self):
        idx = self.member_list.currentRow()
        if idx < 0: return
        m = self.team.members[idx]

        name, ok = QInputDialog.getText(self, "Edit Member", "Member name:", text=m.name)
        if not ok or not name.strip(): return
        email, ok = QInputDialog.getText(self, "Edit Member", "Member email:", text=m.email)
        if not ok or not email.strip(): return

        m.name, m.email = name.strip(), email.strip()
        self._refresh_members()

    def _delete_member(self):
        idx = self.member_list.currentRow()
        if idx < 0: return
        m = self.team.members[idx]
        if QMessageBox.question(
            self, "Delete Member", f"Delete member '{m.name}'?",
            QMessageBox.Yes|QMessageBox.No
        ) == QMessageBox.Yes:
            del self.team.members[idx]
            self._refresh_members()

    def _save(self):
        new_name = self.name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Invalid", "Team name cannot be blank.")
            return
        self.team.name = new_name
        self.accept()
