from enum import Enum


class Setting(Enum):
    NONE = None
    LAB = 'Lab' 
    HOME = 'Home' 
    CLASSROOM = 'Classroom' 
    OUTDOOR = 'Outdoor' 
    CLINIC = 'Clinic'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_name(cls, value):
        return cls._value2member_map_[value]
