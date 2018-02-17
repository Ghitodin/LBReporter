from PyQt5.QtWidgets import QMainWindow, QMessageBox

from AppConfig import APP_NAME
from Settings import AppSettings
from ui.autogen_ui.Ui_MainWindow import Ui_MainWindow
from ui.settings_dialog.SettingsDialog import SettingsDialog


class MainWindow(QMainWindow):
    app_settings = AppSettings()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # init ui:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # set action events:
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSettings.triggered.connect(self.open_settings_dialog)

    def open_settings_dialog(self):
        try:
            settings_dialog = SettingsDialog(app_settings=self.app_settings)
            settings_dialog.exec()
        except ValueError:
            QMessageBox.warning(self, APP_NAME, 'Something wrong', QMessageBox.Ok)