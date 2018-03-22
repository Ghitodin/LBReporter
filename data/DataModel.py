from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    username = Column(String(50), primary_key=True)
    url = Column(String(250), nullable=False)
    feedback_score = Column(String(250), nullable=False)
    feedback_count = Column(String(250), nullable=False)
    trade_volume = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=False)

    def __init__(self, username=None, url=None, feedback_score=None,
                 feedback_count=None, trade_volume=None, created_at=None):
        self.username = username
        self.url = url
        self.feedback_score = feedback_score
        self.feedback_count = feedback_count
        self.trade_volume = trade_volume
        self.created_at = created_at

    def is_empty(self):
        return self.username is None or\
               self.url is None or\
               self.feedback_score is None or\
               self.feedback_count is None or\
               self.created_at is None

    @staticmethod
    def parse_from_json(json):
        new_user = User()
        if json is None:
            return new_user

        if 'error' in json:
            return new_user

        json_data = json['data']
        new_user.username = str(json_data['username'])
        new_user.url = str('<a href=\"' + json_data['url'] + '\"''>Link</a>')
        new_user.feedback_score = str(json_data['feedback_score'])
        new_user.feedback_count = str(json_data['feedback_count'])
        new_user.trade_volume = str(json_data['trade_volume_text'])
        new_user.created_at = str(json_data['created_at'])
        return new_user

    def __repr__(self):
        return 'User(username=%s, url=%s)' % (self.username, self.url)


class Trade(Base):
    __tablename__ = 'trades'
    trade_id = Column(Integer, primary_key=True)  # the contact_id in api json
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
    fee_btc = Column(Float, nullable=False)  # on adv owner
    payment_method = Column(String(250), nullable=False)
    is_buying = Column(Boolean, nullable=False)
    reference_code = Column(String(250), nullable=False)
    owner_username = Column(String(50), ForeignKey('users.username'))
    user = relationship(User)

    def __init__(self, trade_id, seller_username, buyer_username,
                 adv_owner_username, trade_type, created_at,
                 released_at, escrowed_at, exchange_rate_updated_at,
                 currency, amount_currency,
                 amount_btc, fee_btc, payment_method, is_buying,
                 reference_code):
        self.trade_id = trade_id
        self.seller_username = seller_username
        self.buyer_username = buyer_username
        self.adv_owner_username = adv_owner_username
        self.trade_type = trade_type
        self.created_at = created_at
        self.released_at = released_at
        self.escrowed_at = escrowed_at
        self.exchange_rate_updated_at = exchange_rate_updated_at
        self.currency = currency
        self.amount_currency = amount_currency
        self.amount_btc = amount_btc
        self.fee_btc = fee_btc
        self.payment_method = payment_method
        self.is_buying = is_buying
        self.reference_code = reference_code

    def is_adv_owner(self, username):
        return self.adv_owner_username is username

    def set_owner_username(self, username):
        self.owner_username = username

    def get_btc_exchange_rate(self):
        if self.amount_currency is None or self.amount_btc is None:
            return None

        return float(self.amount_currency) / float(self.amount_currency)

    @staticmethod
    def parse_from_json(json):
        if json is None:
            return None

        if 'error' in json:
            return None

        tradeslist_json = json['data']['contact_list']
        for trade_json in tradeslist_json:
            yield Trade(trade_id=trade_json['data']['contact_id'],
                        seller_username=trade_json['data']['seller']['username'],
                        buyer_username=trade_json['data']['buyer']['username'],
                        adv_owner_username=trade_json['data']['advertisement']['advertiser']['username'],
                        trade_type=trade_json['data']['advertisement']['trade_type'],
                        created_at=trade_json['data']['created_at'],
                        released_at=trade_json['data']['released_at'],
                        escrowed_at=trade_json['data']['escrowed_at'],
                        exchange_rate_updated_at=trade_json['data']['exchange_rate_updated_at'],
                        currency=trade_json['data']['currency'],
                        amount_currency=float(trade_json['data']['amount']),
                        amount_btc=float(trade_json['data']['amount_btc']),
                        fee_btc=float(trade_json['data']['fee_btc']),
                        payment_method=trade_json['data']['advertisement']['payment_method'],
                        is_buying=trade_json['data']['is_buying'],
                        reference_code=trade_json['data']['reference_code']
                        )

    def __repr__(self):
        return 'Trade(trade_id=%s, adv_owner_username=%s, trade_type=%s,' \
               ' currency=%s, amount_currency=%s, amount_btc=%s, fee_btc=%s)'\
         % (self.trade_id, self.adv_owner_username, self.trade_type, self.currency,
            self.amount_currency, self.amount_btc, self.fee_btc)
