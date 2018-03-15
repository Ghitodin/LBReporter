from PyQt5.QtCore import QStandardPaths, QDir
from sqlalchemy import create_engine

from AppConfig import ORG_NAME, APP_NAME
from EventLogger import EventLogger
from data.DataModel import Base
from data.source.TradesDataSource import TradesDataSource

__db_name = APP_NAME + '_cache.db'
__db_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + \
            '/' + ORG_NAME + '/' + APP_NAME
__db_file_path = __db_path + '/' + __db_name
__db_dir = QDir(__db_path)

print(__db_path)

if not __db_dir.exists():
    if not __db_dir.mkpath(__db_path):
        EventLogger.show_warning("Can't create a cache, access denied!")

engine = create_engine('sqlite:///' + __db_path + '/' + __db_name)
Base.metadata.create_all(engine)


class TradesDao:
    pass


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