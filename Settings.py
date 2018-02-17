from PyQt5.QtCore import QSettings

from AppConfig import ORG_NAME, APP_NAME


class AppSettings:
    hmac = None
    settings = QSettings(ORG_NAME, APP_NAME)
    __HMAC_VALUE_NAME = 'hmac'

    def __init__(self):
        hmac = self.settings.value(self.__HMAC_VALUE_NAME, self.hmac)
        if hmac is None:
            self.hmac = ''
        else:
            self.hmac = hmac

    def __del__(self):
        self.settings.setValue(self.__HMAC_VALUE_NAME, self.hmac)