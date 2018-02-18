from PyQt5.QtWidgets import QMainWindow, QMessageBox
from lbcapi import api

from AppConfig import APP_NAME
from Settings import AppSettings
from User import User
from ui.autogen_ui.Ui_MainWindow import Ui_MainWindow
from ui.settings_dialog.SettingsDialog import SettingsDialog


class MainWindow(QMainWindow):
    app_settings = AppSettings()
    user = User()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # init ui:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        # set action events:
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSettings.triggered.connect(self.open_settings_dialog)
        self.ui.actionUpdate.triggered.connect(self.test_connection)

    def open_settings_dialog(self):
        try:
            settings_dialog = SettingsDialog(app_settings=self.app_settings)
            settings_dialog.on_data_changed.connect(self.test_connection)
            settings_dialog.exec()
        except ValueError:
            QMessageBox.warning(self, APP_NAME, 'Something wrong', QMessageBox.Ok)

    def init_ui(self):
        self.draw_user(self.user)

    def test_connection(self):
        print('Test connection clicked')

        if self.app_settings.hmac == '' or self.app_settings.hmac_secret == '':
            print("Wrong hmac or hmac secret")
            return

        conn = api.hmac(self.app_settings.hmac, self.app_settings.hmac_secret)
        answer = conn.call('GET', '/api/myself/').json()
        if answer is None:
            print("Api error!")
        else:
            print(answer)

    def draw_user(self, user):
        pass