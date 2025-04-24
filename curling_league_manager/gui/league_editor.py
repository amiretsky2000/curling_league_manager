# curling_league_manager/gui/league_editor.py
import json
from pathlib import Path
from curling_league_manager.core.database import dataclass_to_dict
from curling_league_manager.core.models import Team, Member
from PyQt5.QtWidgets import QDialog, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QMessageBox
from curling_league_manager.gui.team_editor import TeamEditorDialog

class LeagueEditorDialog(QDialog):
    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.league = league
        self.setWindowTitle(f"Edit League: {league.name}")
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self):
        self.list_widget = QListWidget()
        import_btn = QPushButton("Import Teams…")
        export_btn = QPushButton("Export Teams…")
        add_btn    = QPushButton("Add Team")
        edit_btn   = QPushButton("Edit Team")
        del_btn    = QPushButton("Delete Team")

        import_btn.clicked.connect(self._import)
        export_btn.clicked.connect(self._export)
        add_btn.clicked.connect(self._add)
        edit_btn.clicked.connect(self._edit)
        del_btn.clicked.connect(self._delete)

        btn_layout = QHBoxLayout()
        for btn in (import_btn, export_btn, add_btn, edit_btn, del_btn):
            btn_layout.addWidget(btn)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def _refresh_list(self):
        self.list_widget.clear()
        for t in self.league.teams:
            self.list_widget.addItem(f"{t.name} [{t.id[:6]}]")

    def _add(self):
        name, ok = QInputDialog.getText(self, "Add Team", "Team name:")
        if ok and name.strip():
            from curling_league_manager.core.models import Team
            self.league.teams.append(Team(name=name.strip()))
            self._refresh_list()

    def _edit(self):
        idx = self.list_widget.currentRow()
        if idx < 0: return
        dlg = TeamEditorDialog(self.league.teams[idx], parent=self)
        dlg.exec_()
        self._refresh_list()

    def _delete(self):
        idx = self.list_widget.currentRow()
        if idx < 0: return
        team = self.league.teams[idx]
        if QMessageBox.question(self, "Delete Team",
           f"Delete team '{team.name}'?", QMessageBox.Yes|QMessageBox.No
        ) == QMessageBox.Yes:
            del self.league.teams[idx]
            self._refresh_list()

        def _import(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Teams", "", "JSON Files (*.json)")
        if not path:
            return
        # Load list of team-dicts from JSON
        data = json.loads(Path(path).read_text())
        # Rebuild Team and Member objects
        self.league.teams = []
        for team_dict in data:
            team = Team(id=team_dict.get("id"), name=team_dict["name"])
            # reconstruct members
            for m in team_dict.get("members", []):
                team.members.append(Member(id=m.get("id"), name=m["name"], email=m["email"]))
            self.league.teams.append(team)
        self._refresh_list()

    def _export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Teams", "", "JSON Files (*.json)")
        if not path:
            return
        # Convert each Team (+ members) into plain dicts
        data = [dataclass_to_dict(team) for team in self.league.teams]
        Path(path).write_text(json.dumps(data, indent=2))
