from enum import Enum


class Term(Enum):
    FULL_TERM = "Full term",
    PRETERM = "Preterm"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
