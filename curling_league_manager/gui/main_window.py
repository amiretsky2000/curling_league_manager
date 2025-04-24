# curling_league_manager/gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QInputDialog
from curling_league_manager.gui.league_editor import LeagueEditorDialog

class MainWindow(QMainWindow):
    def __init__(self, database, parent=None):
        super().__init__(parent)
        self.database = database
        self.setWindowTitle("Curling League Manager")
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self):
        self.list_widget = QListWidget()
        add_btn    = QPushButton("Add League")
        edit_btn   = QPushButton("Edit League")
        del_btn    = QPushButton("Delete League")
        load_btn   = QPushButton("Load…")
        save_btn   = QPushButton("Save…")

        add_btn.clicked.connect(self._add_league)
        edit_btn.clicked.connect(self._edit_league)
        del_btn.clicked.connect(self._delete_league)
        load_btn.clicked.connect(self._load_db)
        save_btn.clicked.connect(self._save_db)

        btn_layout = QHBoxLayout()
        for btn in (add_btn, edit_btn, del_btn, load_btn, save_btn):
            btn_layout.addWidget(btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(btn_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _refresh_list(self):
        self.list_widget.clear()
        for league in self.database.leagues:
            self.list_widget.addItem(f"{league.name} [{league.id[:6]}]")

    def _add_league(self):
        name, ok = QInputDialog.getText(self, "Add League", "League name:")
        if ok and name.strip():
            self.database.add_league(name.strip())
            self._refresh_list()

    def _edit_league(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            return
        dlg = LeagueEditorDialog(self.database.leagues[idx], parent=self)
        dlg.exec_()
        self._refresh_list()

    def _delete_league(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            return
        league = self.database.leagues[idx]
        confirm = QMessageBox.question(self, "Delete League",
            f"Delete league '{league.name}'?", QMessageBox.Yes|QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.database.remove_league(league.id)
            self._refresh_list()

    def _load_db(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "JSON Files (*.json)")
        if path:
            self.database.load(path)
            self._refresh_list()

    def _save_db(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Database", "", "JSON Files (*.json)")
        if path:
            self.database.save(path)
