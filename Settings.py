from PyQt5.QtCore import QSettings

from AppConfig import ORG_NAME, APP_NAME


class AppSettings:
    hmac = None
    hmac_secret = None
    settings = QSettings(ORG_NAME, APP_NAME)
    __HMAC_VALUE_NAME = 'hmac'
    __HMAC_SECRET_VALUE_NAME = 'hmac_secret'

    def __init__(self):
        self.hmac = self.settings.value(self.__HMAC_VALUE_NAME, self.hmac)
        self.hmac_secret = self.settings.value(self.__HMAC_SECRET_VALUE_NAME, self.hmac_secret)
        if self.hmac is None:
            self.hmac = ''
        if self.hmac_secret is None:
            self.hmac_secret = ''

    def __del__(self):
        self.settings.setValue(self.__HMAC_VALUE_NAME, self.hmac)
        self.settings.setValue(self.__HMAC_SECRET_VALUE_NAME, self.hmac_secret)