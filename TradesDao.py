from PyQt5.QtCore import QStandardPaths
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from AppConfig import ORG_NAME, APP_NAME

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


# TODO: need to create the database if it does not exist on this path:
print(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation) +
                       '\\' + ORG_NAME + '\\' + APP_NAME + '\\test_db.db')

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
#engine = create_engine('sqlite:///C:\\path\\to\\database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
#Base.metadata.create_all(engine)


class TradesDao:
    pass