
class Trade:
    id = None  # the contact_id in api json
    seller_username = None
    buyer_username = None
    adv_owner_username = None
    trade_type = None
    created_at = None
    released_at = None
    escrowed_at = None
    exchange_rate_updated_at = None
    currency = None
    amount_currency = None
    amount_btc = None
    fee_btc = None  # on adv owner
    payment_method = None
    is_buying = None
    reference_code = None

    def __init__(self, id, seller_username, buyer_username,
                 adv_owner_username, trade_type, created_at,
                 released_at, escrowed_at, exchange_rate_updated_at,
                 currency, amount_currency,
                 amount_btc, fee_btc, payment_method, is_buying,
                 reference_code):
        self.id = id
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
            yield Trade(id=trade_json['data']['contact_id'],
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
        return 'Trade(id=%s, adv_owner_username=%s, trade_type=%s,' \
               ' currency=%s, amount_currency=%s, amount_btc=%s, fee_btc=%s)'\
         % (self.id, self.adv_owner_username, self.trade_type, self.currency,
            self.amount_currency, self.amount_btc, self.fee_btc)