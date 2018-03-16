from PyQt5.QtCore import QStandardPaths, QDir, QObject, pyqtSignal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from AppConfig import ORG_NAME, APP_NAME
from EventLogger import EventLogger
from data.DataModel import Base, Trade, User
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
session_factory = sessionmaker(bind=engine)


class TradesDao:
    def get_trades(self, session, username):
        return session.query(Trade).join(username).order_by(Trade.released_at).all()

    def get_trade_by_id(self, session, username, trade_id):
        pass

    def get_last(self, session, username):
        pass

    def insert_trades(self, session, trades):
        session.add_all(trades)
        session.commit()

    def update_trade(self, session, username, trade):
        pass


class UserDao:
    def get_user(self, session, username):
        return session.query(User).filter(User.username == username)

    def insert_user(self, session, user):
        cached_user = session.query(User).filter(User.username == user.username)
        if not cached_user.count():
            session.add(user)
        else:
            pass  # TODO: need to update user

        session.commit()


class TradesLocalDataSource(TradesDataSource, QObject):
    class __TradesLocalDataSource:
        # signals:
        on_data_not_available = pyqtSignal()
        on_trade_loaded = pyqtSignal(Trade)
        on_all_trades_loaded = pyqtSignal(list)

        __trades_dao = TradesDao()
        __user_dao = UserDao()

        def save_trades(self, trades, trades_owner):
            session = session_factory()
            map(lambda i: i.set_owner_username(trades_owner.username), trades)
            try:
                self.__user_dao.insert_user(session, trades_owner)
                self.__trades_dao.insert_trades(session, trades)
            except Exception as e:
                print(type(e))
                print(e)
                session.rollback()
                raise
            finally:
                session.close()

        def get_all_trades(self, username):
            session = session_factory()
            trades = self.__trades_dao.get_trades(session)
            session.close()
            if not trades:
                self.on_data_not_available.emit()
                return

            self.on_all_trades_loaded.emit(trades)

    instance = None

    def __new__(cls):
        if not TradesLocalDataSource.instance:
            TradesLocalDataSource.instance = TradesLocalDataSource.__TradesLocalDataSource()
        return TradesLocalDataSource.instance
