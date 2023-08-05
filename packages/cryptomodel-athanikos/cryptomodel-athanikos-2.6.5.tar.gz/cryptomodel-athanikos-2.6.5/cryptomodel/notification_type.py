from enum import Enum


class NOTIFICATION_TYPE(Enum):
    BALANCE = "BALANCE"
    SYMBOL_VALUE_DROP = "SYMBOL_VALUE_DROP"
    SYMBOL_VALUE_INCREASE = "SYMBOL_VALUE_INCREASE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)