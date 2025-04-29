import sys
from PyQt5.QtWidgets import QApplication
from .database import Database
from .auth_window import AuthWindow
from .main_window import MainWindow

class Launcher:
    def __init__(self):
        self.db = Database()
        self.app = QApplication(sys.argv)
        
        self.auth_window = AuthWindow(self.db, self.on_auth_success)
        self.main_window = None

    def on_auth_success(self, username):
        self.auth_window.hide()
        self.main_window = MainWindow(self.db, username)
        self.main_window.show()

    def run(self):
        self.auth_window.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()