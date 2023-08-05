from enum import Enum


class ORDER_TYPES(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
