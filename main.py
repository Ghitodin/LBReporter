import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from ui.autogen_ui.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


a = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(a.exec())