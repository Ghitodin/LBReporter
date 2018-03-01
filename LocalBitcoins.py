# lbcapi wrapper
from threading import Thread, Timer

from PyQt5.QtCore import QObject, pyqtSignal
from lbcapi import api
from requests.exceptions import ConnectionError

from data_model.Trade import Trade
from data_model.User import User


class LocalBitcoins(QObject):

    # signals:
    on_error_occurred = pyqtSignal(str)
    on_user_received = pyqtSignal(User)
    on_request_started = pyqtSignal()
    on_request_finished = pyqtSignal()

    __request_failures_counter = 0
    __REQUEST_REPEAT_DELAY_SEC = 3.0

    def get_user(self, hmac, hmac_secret, repeat_if_failure=True):
        self.__checkKeys(hmac, hmac_secret)

        self.on_request_started.emit()
        thread = Thread(target=self.__thread_worker, args=(hmac, hmac_secret, 'GET', '/api/myself/',
                                                           self.__on_get_user_finished, repeat_if_failure),
                        daemon=True)
        thread.start()

    def get_released_trades_test(self, hmac, hmac_secret, repeat_if_failure=False):
        self.__checkKeys(hmac, hmac_secret)
        thread = Thread(target=self.__thread_worker, args=(hmac, hmac_secret, 'GET', '/api/dashboard/released/',
                                                           self.__on_get_released_trades_finished, repeat_if_failure),
                        daemon=True)
        thread.start()

    def __thread_worker(self, hmac, hmac_secret, method, url, on_finished_callback, repeat_if_failure):
        try:
            conn = api.hmac(hmac, hmac_secret)
            on_finished_callback(conn.call(method, url).json())
        except ConnectionError:
            if self.__request_failures_counter is 0:  # is first error
                self.on_error_occurred.emit('No network access')

            self.__request_failures_counter += 1
            if repeat_if_failure is True:
                thread = Timer(self.__REQUEST_REPEAT_DELAY_SEC,
                               function=self.__thread_worker, args=(hmac, hmac_secret, method, url,
                                                                    on_finished_callback, repeat_if_failure))
                thread.start()
        except Exception:
            self.on_error_occurred.emit('Internal API error!')
        else:
            self.__request_failures_counter = 0

    def __on_get_user_finished(self, json):
        try:
            error = LocalBitcoins.ServerError.parse_prom_json(json)
            if error is not None:
                self.on_error_occurred.emit(error.message)
                return

            user = User.parse_from_json(json)
            self.on_user_received.emit(user)
            self.on_request_finished.emit()

        except KeyError:
            self.on_error_occurred.emit('Wrong response format! Need to update the App.')

    def __on_get_released_trades_finished(self, json):
        print(json)
        trades = Trade.parse_from_json(json)
        for trade in trades:
            print(trade)

    def __get_error(self):
        pass

    def __checkKeys(self, hmac, hmac_secret):
        if hmac == '' or hmac_secret == '':
            self.on_error_occurred.emit("Wrong hmac or hmac secret")
            return

    class ServerError:
        message = None
        error_code = None

        def __init__(self, message=None, error_code=None):
            self.message = message
            self.error_code = error_code

        @staticmethod
        def parse_prom_json(json):
            if 'error' in json:
                json_error = json['error']
                return LocalBitcoins.ServerError(json_error['message'], json_error['error_code'])
            return None
