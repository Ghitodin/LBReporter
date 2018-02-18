from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog

from ui.autogen_ui.Ui_SettingsDialog import Ui_SettingsDialog


class SettingsDialog(QDialog):
    __app_settings = None

    # signal
    on_data_changed = pyqtSignal()

    def __init__(self, app_settings, parent=None):
        super(SettingsDialog, self).__init__(parent)

        if app_settings is None:
            raise ValueError('Settings is not created')

        self.__app_settings = app_settings

        # init ui:
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        # slots:
        self.ui.buttonBox.accepted.connect(self.save_settings)

        # set up start values:
        self.ui.hmacEdit.setText(self.__app_settings.hmac)
        self.ui.hmacSecretEdit.setText(self.__app_settings.hmac_secret)

    def save_settings(self):
        is_data_changed = False
        new_hmac = self.ui.hmacEdit.text()
        if self.__app_settings.hmac != new_hmac:
            self.__app_settings.hmac = new_hmac
            is_data_changed = True

        new_hmac_secret = self.ui.hmacSecretEdit.text();
        if self.__app_settings.hmac_secret != new_hmac_secret:
            self.__app_settings.hmac_secret = new_hmac_secret
            is_data_changed = True

        if is_data_changed:
            self.on_data_changed.emit()