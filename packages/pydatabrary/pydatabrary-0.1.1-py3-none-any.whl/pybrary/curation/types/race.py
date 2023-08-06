from enum import Enum


class Race(Enum):
    NONE = None
    AMERICAN_INDIAN_OR_ALASKA_NATIVE = 'American Indian or Alaska Native'
    ASIAN = 'Asian'
    NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER = 'Native Hawaiian or Other Pacific Islander'
    BLACK_OR_AFRICAN_AMERICAN = 'Black or African American'
    WHITE = 'White'
    MORE_THAN_ONE = 'More than one'
    UNKNOWN_OR_NOT_REPORTED = 'Unknown or not reported'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
