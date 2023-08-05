from mongoengine import *
from keyring import get_password


class EUR(EmbeddedDocument):
    meta = {'strict': False}
    price = FloatField()
    volume_24h = FloatField()
    percent_change_1h = FloatField()
    percent_change_24h = FloatField()
    percent_change_7d = FloatField()
    market_cap = FloatField()
    last_updated = StringField()


class EURQuote(EmbeddedDocument):
    meta = {'strict': False}
    eur = EmbeddedDocumentField(EUR, db_field='EUR')


class Coin(EmbeddedDocument):
    meta = {'strict': False}
    id = IntField()
    name = StringField()
    symbol = StringField()
    quote = EmbeddedDocumentField(EURQuote, db_field='quote')


class Status(EmbeddedDocument):
    meta = {'strict': False}
    timestamp = StringField()


class prices(Document):
    meta = {'strict': False}
    _id = IntField(db_field='_id')
    coins = EmbeddedDocumentListField(Coin, db_field='data')
    status = ListField(EmbeddedDocumentListField(Status, db_field='status'))


operators = {'>': 'greater', '<': 'less', '=': 'equal'}
change_type = {'1': 'increase', '2': 'decrease', '3': 'increase_and_decrease'}
notification_type = {'telegram': 'telegram'}
operation_type = {'1': 'Added', '2': 'Modified', '3': 'Deleted'}


class user_settings(Document):
    meta = {'strict': False}
    userId = IntField()
    preferred_currency = StringField()


class user_notification(Document):
    meta = {'strict': False}
    userId = IntField()
    user_name = StringField()
    user_email = StringField()
    condition_value = LongField()
    field_name = StringField()
    operator = StringField(choices=operators.keys())
    notify_times = LongField()
    notify_every_in_seconds = LongField()
    symbol = StringField()
    last_date_sent = DateField()
    is_active = BooleanField()
    times_sent = IntField()
    channel_type = StringField()


class user_transaction(Document):
    meta = {'strict': False}
    user_id = IntField()
    volume = LongField()
    symbol = StringField()
    value = LongField()
    price = LongField()
    date = DateField()
    source = StringField()
    currency = StringField()
    source_id = StringField()
    operation = StringField()


class user_channel(Document):
    meta = {'strict': False}
    user_id = IntField()
    channel_type = StringField()
    chat_id = StringField()
    user_email = StringField()

    def set_token(self):
        self.token = get_password(self.notification_type, 'token')


class user_settings(Document):
    user_id = IntField()
    preferred_currency = StringField()


class total_symbol_value:

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['exchange_rates']
        del state['symbol_prices']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __init__(self, user_id, date_time_calculated, preferred_currency, symbol_prices, exchange_rates):
        self.symbol_prices = symbol_prices
        self.exchange_rates = exchange_rates
        self.user_id = user_id
        self.converted_currency = preferred_currency
        self.converted_value = 0
        self.date_time_calculated = date_time_calculated
        self.user_grouped_symbol_values = []

    def create(self, transactions):
        for trans in transactions:  # pythonic ? iterators?
            self.add_transaction(trans)
        return self

    def add_transaction(self, transaction):
        computed_usv = user_symbol_value(user_id=self.user_id, transaction=transaction,
                                         present_price=self.symbol_prices[transaction.symbol].price,
                                         currency=self.converted_currency, exchange_rates=self.exchange_rates,
                                         date_time_calculated=self.date_time_calculated,
                                         converted_currency=self.converted_currency)

        ugsv = self.contains_symbol(transaction)

        if ugsv is not None:
            ugsv.volume += computed_usv.user_transaction.volume
            ugsv.value += computed_usv.converted_value
            ugsv.converted_currency = self.converted_currency
        else:
            ugsv = user_grouped_symbol_value(user_id=self.user_id, volume=transaction.volume,
                                             price=self.symbol_prices[transaction.symbol].price,
                                             currency=self.converted_currency,
                                             date_time_calculated=self.date_time_calculated, symbol=transaction.symbol)
            self.user_grouped_symbol_values.append(ugsv)

        self.converted_value += computed_usv.converted_value
        ugsv.user_symbol_values.append(computed_usv)

    def contains_symbol(self, transaction):
        if self.user_grouped_symbol_values is None:
            return None
        if len(self.user_grouped_symbol_values) == 0:
            return None

        for item in self.user_grouped_symbol_values:
            if item.symbol == transaction.symbol:
                return item
        return None


class user_grouped_symbol_value:
    def __init__(self, user_id, symbol, volume, price, currency, date_time_calculated):
        self.value = 0
        self.symbol = symbol
        self.volume = volume
        self.date_time_calculated = date_time_calculated
        self.user_id = user_id
        self.currency = currency
        self.price = price
        self.converted_currency = ""
        self.converted_value = 0
        self.user_symbol_values = []


class user_symbol_value:
    def __init__(self, user_id, transaction, present_price,
                 currency, date_time_calculated, converted_currency, cc):
        self.user_transaction = transaction
        self.present_price = present_price
        self.currency = currency
        self.date_time_calculated = date_time_calculated
        self.value = self.present_price * self.user_transaction.volume
        self.user_id = user_id
        self.converted_currency = converted_currency
        self.cc = cc  # fix it static / singleton
        self.converted_value = cc.convert_value(self.value, self.currency, self.converted_currency)


class Rates(EmbeddedDocument):
    meta = {'strict': False}
    AED = FloatField()
    AFN = FloatField()
    ALL = FloatField()
    AMD = FloatField()
    ANG = FloatField()
    AOA = FloatField()
    ARS = FloatField()
    AUD = FloatField()
    AWG = FloatField()
    AZN = FloatField()
    BAM = FloatField()
    BBD = FloatField()
    BDT = FloatField()
    BGN = FloatField()
    BHD = FloatField()
    BIF = FloatField()
    BMD = FloatField()
    BND = FloatField()
    BOB = FloatField()
    BRL = FloatField()
    BSD = FloatField()
    BTC = FloatField()
    BTN = FloatField()
    BWP = FloatField()
    BYN = FloatField()
    BYR = FloatField()
    BZD = FloatField()
    CAD = FloatField()
    CDF = FloatField()
    CHF = FloatField()
    CLF = FloatField()
    CLP = FloatField()
    CNY = FloatField()
    COP = FloatField()
    CRC = FloatField()
    CUC = FloatField()
    CUP = FloatField()
    CVE = FloatField()
    CZK = FloatField()
    DJF = FloatField()
    DKK = FloatField()
    DOP = FloatField()
    DZD = FloatField()
    EGP = FloatField()
    ERN = FloatField()
    ETB = FloatField()
    EUR = FloatField()
    FJD = FloatField()
    FKP = FloatField()
    GBP = FloatField()
    GEL = FloatField()
    GGP = FloatField()
    GHS = FloatField()
    GIP = FloatField()
    GMD = FloatField()
    GNF = FloatField()
    GTQ = FloatField()
    GYD = FloatField()
    HKD = FloatField()
    HNL = FloatField()
    HRK = FloatField()
    HTG = FloatField()
    HUF = FloatField()
    IDR = FloatField()
    ILS = FloatField()
    IMP = FloatField()
    INR = FloatField()
    IQD = FloatField()
    IRR = FloatField()
    ISK = FloatField()
    JEP = FloatField()
    JMD = FloatField()
    JOD = FloatField()
    JPY = FloatField()
    KES = FloatField()
    KGS = FloatField()
    KHR = FloatField()
    KMF = FloatField()
    KPW = FloatField()
    KRW = FloatField()
    KWD = FloatField()
    KYD = FloatField()
    KZT = FloatField()
    LAK = FloatField()
    LBP = FloatField()
    LKR = FloatField()
    LRD = FloatField()
    LSL = FloatField()
    LTL = FloatField()
    LVL = FloatField()
    LYD = FloatField()
    MAD = FloatField()
    MDL = FloatField()
    MGA = FloatField()
    MKD = FloatField()
    MMK = FloatField()
    MNT = FloatField()
    MOP = FloatField()
    MRO = FloatField()
    MUR = FloatField()
    MVR = FloatField()
    MWK = FloatField()
    MXN = FloatField()
    MYR = FloatField()
    MZN = FloatField()
    NAD = FloatField()
    NGN = FloatField()
    NIO = FloatField()
    NOK = FloatField()
    NPR = FloatField()
    NZD = FloatField()
    OMR = FloatField()
    PAB = FloatField()
    PEN = FloatField()
    PGK = FloatField()
    PHP = FloatField()
    PKR = FloatField()
    PLN = FloatField()
    PYG = FloatField()
    QAR = FloatField()
    RON = FloatField()
    RSD = FloatField()
    RUB = FloatField()
    RWF = FloatField()
    SAR = FloatField()
    SBD = FloatField()
    SCR = FloatField()
    SDG = FloatField()
    SEK = FloatField()
    SGD = FloatField()
    SHP = FloatField()
    SLL = FloatField()
    SOS = FloatField()
    SRD = FloatField()
    STD = FloatField()
    SVC = FloatField()
    SYP = FloatField()
    SZL = FloatField()
    THB = FloatField()
    TJS = FloatField()
    TMT = FloatField()
    TND = FloatField()
    TOP = FloatField()
    TRY = FloatField()
    TTD = FloatField()
    TWD = FloatField()
    TZS = FloatField()
    UAH = FloatField()
    UGX = FloatField()
    USD = FloatField()
    UYU = FloatField()
    UZS = FloatField()
    VEF = FloatField()
    VND = FloatField()
    VUV = FloatField()
    WST = FloatField()
    XAF = FloatField()
    XAG = FloatField()
    XAU = FloatField()
    XCD = FloatField()
    XDR = FloatField()
    XOF = FloatField()
    XPF = FloatField()
    YER = FloatField()
    ZAR = FloatField()
    ZMK = FloatField()
    ZMW = FloatField()
    ZWL = FloatField()


class exchange_rates(Document):
    meta = {'strict': False}
    _id = IntField(db_field='_id')
    success = BooleanField()
    base = StringField()
    rates = EmbeddedDocumentField(Rates, db_field='rates')
    date = StringField()


class SymbolRates:
    def __init__(self, date):
        self.date = date
        self.rates = {}

    def add_rate(self, symbol, metrics):
        self.rates.update({symbol: metrics})


class SymbolMetrics:
    def __init__(self, price, volume_24h, percent_change_1h,
                 percent_change_24h, percent_change_7d, market_cap):
        self.price = price
        self.volume_24h = volume_24h
        self.percent_change_1h = percent_change_1h
        self.percent_change_24h = percent_change_24h
        self.percent_change_7d = percent_change_7d
        self.market_cap = market_cap
