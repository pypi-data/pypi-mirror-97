from enum import Enum


class CHANNEL_TYPE(Enum):
    TELEGRAM = "TELEGRAM"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)