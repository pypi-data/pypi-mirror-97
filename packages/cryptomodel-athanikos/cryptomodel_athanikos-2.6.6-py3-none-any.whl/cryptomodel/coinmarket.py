from mongoengine import *
from cryptomodel.operations import OPERATIONS


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
    timestamp = IntField()


class prices(Document):
    meta = {'strict': False}
    coins = EmbeddedDocumentListField(Coin, db_field='data')
    status = EmbeddedDocumentField(Status, db_field='status')
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())

    def __init__(self, coins, status, source_id, operation, *args, **kwargs):
        super(prices, self).__init__(*args, **kwargs)
        self.coins = coins
        self.status = status
        self.source_id = source_id
        self.operation = operation
