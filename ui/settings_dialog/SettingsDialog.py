from PyQt5.QtWidgets import QDialog

from ui.autogen_ui.Ui_SettingsDialog import Ui_SettingsDialog


class SettingsDialog(QDialog):
    __app_settings = None

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

    def save_settings(self):
        print(self.ui.hmacEdit.text())
        self.__app_settings.hmac = self.ui.hmacEdit.text()