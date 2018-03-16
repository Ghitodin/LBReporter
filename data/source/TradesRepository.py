from data.source.Local import TradesLocalDataSource
from data.source.TradesDataSource import TradesDataSource


class TradesRepository:

    class __TradeRepository(TradesDataSource):
        __trades_local_data_source = None
        __cached_last_trade = None
        __is_valid_cache = False

        def __init__(self):
            self.__trades_local_data_source = TradesLocalDataSource()

        def save_trades(self, trades, trades_owner):
            self.__trades_local_data_source.save_trades(trades, trades_owner)

        def get_last_trade(self, username):
            if self.__is_valid_cache is True and self.__cached_last_trade is not None:
                self.on_trades_loaded.emit([self.__cached_last_trade])
                return

    instance = None

    def __new__(cls):
        if not TradesRepository.instance:
            TradesRepository.instance = TradesRepository.__TradeRepository()
        return TradesRepository.instance
