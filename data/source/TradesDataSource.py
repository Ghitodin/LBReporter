from PyQt5.QtCore import pyqtSignal


class TradesDataSource:

    on_trades_loaded = pyqtSignal(list)

    def get_all_trades(self, username):
        pass

    def get_trades(self, count, username):
        pass

    def get_last_trade(self, username):
        pass

    def save_trades(self, trades, username):
        pass