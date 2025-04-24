# run_gui.py
import sys
from PyQt5.QtWidgets import QApplication
from curling_league_manager.gui.main_window import MainWindow
from curling_league_manager.core.database import LeagueDatabase

def main():
    db = LeagueDatabase()
    app = QApplication(sys.argv)
    win = MainWindow(database=db)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
