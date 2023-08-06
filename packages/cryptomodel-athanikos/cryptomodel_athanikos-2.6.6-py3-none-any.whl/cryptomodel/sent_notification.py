import jsonpickle
from mongoengine import *

from calculator.helpers import if_none_raise
from cryptomodel.computed_notification import computed_notification
from cryptomodel.notification_type import NOTIFICATION_TYPE

'''
Represents a sent notification  
Holds a computed_notifications 
Extends with sent flag and sent_date
'''


class sent_notification(computed_notification):
    meta = {'strict': False}
    sent_date = DateField()
