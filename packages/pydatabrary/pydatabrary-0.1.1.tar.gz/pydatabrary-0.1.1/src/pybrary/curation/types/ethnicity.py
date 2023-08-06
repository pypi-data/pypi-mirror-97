from enum import Enum


class Ethnicity(Enum):
    NONE = None
    NOT_HISPANIC_OR_LATINO = 'Not Hispanic or Latino'
    HISPANIC_OR_LATINO = 'Hispanic or Latino'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
