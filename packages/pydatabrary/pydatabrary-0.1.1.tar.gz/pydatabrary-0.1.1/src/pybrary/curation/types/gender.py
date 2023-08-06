from enum import Enum


class Gender(Enum):
    NONE = None
    FEMALE = 'Female'
    MALE = 'Male'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
