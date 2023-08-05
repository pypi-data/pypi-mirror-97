from enum import Enum


class OPERATIONS(Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    REMOVED = "REMOVED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)
