from enum import Enum


class Category(Enum):
    NONE = None
    PARTICIPANT = 'participant'
    PILOT = 'pilot'
    EXCLUSION = 'exclusion'
    CONDITION = 'condition'
    GROUP = 'group'
    TASK = 'task'
    CONTEXT = 'context'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
