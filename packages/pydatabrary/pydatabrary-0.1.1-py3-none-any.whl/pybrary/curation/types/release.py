from enum import Enum


class Release(Enum):
    NONE = None
    PRIVATE = 'PRIVATE'
    SHARED = 'SHARED'
    EXCERPTS = 'EXCERPTS'
    PUBLIC = 'PUBLIC'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]

