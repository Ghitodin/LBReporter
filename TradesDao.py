from PyQt5.QtCore import QStandardPaths, QDir, QFile
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from AppConfig import ORG_NAME, APP_NAME
from EventLogger import EventLogger

Base = declarative_base()


class UsersTable(Base):
    __tablename__ = 'users'
    username = Column(String(50), primary_key=True)
    url = Column(String(250), nullable=False)
    feedback_score = Column(String(250), nullable=False)
    feedback_count = Column(String(250), nullable=False)
    trade_volume = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=False)


class TradesTable(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    seller_username = Column(String(250), nullable=False)
    buyer_username = Column(String(250), nullable=False)
    adv_owner_username = Column(String(250), nullable=False)
    trade_type = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=False)
    released_at = Column(String(250), nullable=False)
    escrowed_at = Column(String(250), nullable=False)
    exchange_rate_updated_at = Column(String(250), nullable=False)
    currency = Column(String(250), nullable=False)
    amount_currency = Column(Float, nullable=False)
    amount_btc = Column(Float, nullable=False)
    fee_btc = Column(Float, nullable=False)
    payment_method = Column(String(250), nullable=False)
    is_buying = Column(Boolean, nullable=False)
    reference_code = Column(String(250), nullable=False)
    owner_username = Column(Integer, ForeignKey('users.username'))
    user = relationship(UsersTable)


__db_name = APP_NAME + '_cache.db'
__db_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) + \
            '/' + ORG_NAME + '/' + APP_NAME
__db_file_path = __db_path + '/' + __db_name
__db_dir = QDir(__db_path)

print(__db_path)

if not __db_dir.exists():
    if not __db_dir.mkpath(__db_path):
        EventLogger.show_warning("Can't create a cache, access denied!")

__db_file = QFile(__db_file_path)
if not __db_file.exists(__db_file_path):
    engine = create_engine('sqlite:///' + __db_path + '/' + __db_name)
    Base.metadata.create_all(engine)


class TradesDao:
    pass
