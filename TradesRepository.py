from TradesDataSource import TradesDataSource


class TradesRepository(TradesDataSource):
    __cached_last_trade = None
    __is_valid_cache = False

    class __TradeRepository:
        def __init__(self):
            self.test_value = 44

    instance = None

    def __new__(cls):
        if not TradesRepository.instance:
            TradesRepository.instance = TradesRepository.__TradeRepository()
        return TradesRepository.instance

    def save_trades(self, trades, user_name):
        pass

    def get_last_trade(self, username):
        if self.__is_valid_cache is True and self.__cached_last_trade is not None:
            self.on_trades_loaded.emit([self.__cached_last_trade])
            return


class TradesLocalDataSource(TradesDataSource):
    __trades_dao = None

    class __TradesLocalDataSource:
        def __init__(self):
            __trades_dao = TradesDao()

    instance = None

    def __new__(cls):
        if not TradesLocalDataSource.instance:
            TradesLocalDataSource.instance = TradesLocalDataSource.__TradesLocalDataSource()
        return TradesLocalDataSource.instance


class TradesDao:
    pass
