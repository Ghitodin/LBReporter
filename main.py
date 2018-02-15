import PyQt5.QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi()
