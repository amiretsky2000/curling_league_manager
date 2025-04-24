# curling_league_manager/gui/team_editor.py
from PyQt5.QtWidgets import (
    QDialog, QListWidget, QPushButton,
    QFormLayout, QLineEdit, QHBoxLayout,
    QMessageBox, QVBoxLayout, QWidget
)
from curling_league_manager.core.models import Member
from curling_league_manager.gui.member_editor import MemberEditorDialog


class TeamEditorDialog(QDialog):
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.team = team
        self.setWindowTitle(f"Edit Team: {team.name}")
        self._setup_ui()
        self._refresh_members()

    def _setup_ui(self):
        # Top: team-name form
        name_layout = QFormLayout()
        self.name_edit = QLineEdit(self.team.name)
        name_layout.addRow("Team Name:", self.name_edit)

        # Middle: member list
        self.member_list = QListWidget()

        # Member buttons
        add_m = QPushButton("Add Member")
        edit_m = QPushButton("Edit Member")
        del_m = QPushButton("Delete Member")
        add_m.clicked.connect(self._add_member)
        edit_m.clicked.connect(self._edit_member)
        del_m.clicked.connect(self._delete_member)
        m_btn_layout = QHBoxLayout()
        for btn in (add_m, edit_m, del_m):
            m_btn_layout.addWidget(btn)

        # Bottom: save/close team dialog
        btn_save   = QPushButton("Save Team")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(self._save_team)
        btn_cancel.clicked.connect(self.reject)
        t_btn_layout = QHBoxLayout()
        t_btn_layout.addWidget(btn_save)
        t_btn_layout.addWidget(btn_cancel)

        # Assemble everything
        main_layout = QVBoxLayout()
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.member_list)
        main_layout.addLayout(m_btn_layout)
        main_layout.addLayout(t_btn_layout)
        self.setLayout(main_layout)

    def _refresh_members(self):
        self.member_list.clear()
        for m in self.team.members:
            self.member_list.addItem(f"{m.name} <{m.email}>")

    def _add_member(self):
        dlg = MemberEditorDialog(parent=self)
        if dlg.exec_():
            self.team.members.append(dlg.member)
            self._refresh_members()

    def _edit_member(self):
        idx = self.member_list.currentRow()
        if idx < 0:
            return
        existing = self.team.members[idx]
        dlg = MemberEditorDialog(member=existing, parent=self)
        if dlg.exec_():
            # dlg.member is the same object, updated in-place
            self._refresh_members()

    def _delete_member(self):
        idx = self.member_list.currentRow()
        if idx < 0:
            return
        if QMessageBox.question(
            self, "Delete Member",
            "Remove this member?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:
            del self.team.members[idx]
            self._refresh_members()

    def _save_team(self):
        new_name = self.name_edit.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Invalid", "Team name cannot be blank.")
            return
        self.team.name = new_name
        self.accept()
