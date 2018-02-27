from PyQt5.QtCore import QObject, pyqtSignal


class TradesRepository(QObject):
    __cached_last_trade = None
    __is_valid_cache_last_trade = False

    class __TradeRepository:
        def __init__(self):
            self.test_value = 44

    instance = None

    def __new__(cls):
        if not TradesRepository.instance:
            TradesRepository.instance = TradesRepository.__TradeRepository()
        return TradesRepository.instance

    def save_trades(self, trades):
        pass

# TODO: need to extends those classes:
class TradesLocalDataSource:
    pass


class TradesDataSource:

    on_trades_loaded = pyqtSignal()
    on_get_trade = pyqtSignal()

    def get_all_trades(self):
        pass

    def get_trades(self, count):
        pass

    def get_last_trade(self):
        pass

    def save_trades(self, trades):
        pass
