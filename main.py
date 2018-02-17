import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window.MainWindow import MainWindow

a = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(a.exec())