from enum import Enum


class TRANSACTION_TYPES(Enum):
    DEPOSIT = "DEPOSIT"
    TRADE = "TRADE"
    WITHDRAWAL = "WITHDRAWAL"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
