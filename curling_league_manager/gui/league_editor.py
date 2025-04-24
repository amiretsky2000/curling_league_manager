# curling_league_manager/gui/league_editor.py
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
        if path:
            # implement import logic...
            pass

    def _export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Teams", "", "JSON Files (*.json)")
        if path:
            # implement export logic...
            pass
