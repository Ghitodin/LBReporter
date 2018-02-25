# lbcapi wrapper
from threading import Thread
from typing import Type

from PyQt5.QtCore import QObject, pyqtSignal
from lbcapi import api

from User import User


class LocalBitcoins(QObject):
    # signal
    on_user_received = pyqtSignal(User)
    on_error_occurred = pyqtSignal(str)

    def get_user(self, hmac, hmac_secret):
        if hmac == '' or hmac_secret == '':
            self.on_error_occurred.emit("Wrong hmac or hmac secret")
            return

        thread = Thread(target=self.__thread_worker, args=(hmac, hmac_secret, 'GET', '/api/myself/',
                                                           self.__on_get_user_finished))
        thread.start()

    def __thread_worker(self, hmac, hmac_secret, method, url, on_finished_callback):
        conn = api.hmac(hmac, hmac_secret)
        on_finished_callback(conn.call(method, url).json())

    def __on_get_user_finished(self, json):
        # !error check passed
        user = User.parse_from_json(json)
        self.on_user_received.emit(user)