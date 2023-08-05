import jsonpickle
from mongoengine import *

from enum import Enum

from calculator.helpers import if_empty_string_raise
from cryptomodel.operations import OPERATIONS


class EVENT_TYPES(Enum):
    USER_NOTIFICATION = "USER_NOTIFICATION"
    COMPUTED_NOTIFICATION = "COMPUTED_NOTIFICATION"
    SENT_NOTIFICATION = "SENT_NOTIFICATION"
    TRANSACTIONS = "TRANSACTIONS"
    SETTINGS = "SETTINGS"


    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class event_data(EmbeddedDocument):
    type = StringField(choices=EVENT_TYPES.choices())
    operation = StringField(operations=OPERATIONS.choices())
    data = StringField()

'''
Represents an event item for event based communication between microservices 
where key is user_id (used for petitioning)
and data is the string equivalent of the json representation of a data and the event_type 
'''


class event_store(Document):
    meta = {'strict': False}
    key = StringField()
    event_data = EmbeddedDocumentField(event_data, db_field='event_data')

    '''decodes the string json of data to object '''
    def get_data_str_to_obj(self):
        if_empty_string_raise(self.event_data)
        if_empty_string_raise(self.event_data.data)
        return jsonpickle.decode(self.event_data.data)

    @staticmethod
    def create(key, event_type, data, operation):
        es  = event_store()
        es.key = key
        ed = event_data()
        ed.operation = operation
        ed.data = jsonpickle.encode(data)
        ed.type = event_type
        es.event_data = ed
        return es