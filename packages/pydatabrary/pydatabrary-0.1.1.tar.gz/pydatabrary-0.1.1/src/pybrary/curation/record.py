import json
from pybrary.curation.types.category import Category
from pybrary.curation.types.ethnicity import Ethnicity
from pybrary.curation.types.gender import Gender
from pybrary.curation.types.race import Race
from pybrary.curation.types.reason import Reason
from pybrary.curation.types.setting import Setting


class Record:
    def __init__(
            self,
            key,
            category,
            race=Race.UNKNOWN_OR_NOT_REPORTED,
            ethnicity=Ethnicity.NONE,
            gender=Gender.NONE,
            setting=Setting.NONE,
            reason=Reason.NONE,
            name=None,
            birthdate=None,
            disability=None,
            positions=None,
            summary=None,
            description=None,
            language=None,
            country=None,
            state=None,
            gestational_age=None,
            birth_weight=None,
    ):
        if category is None:
            raise Exception('A category is required for a Record')
        self._key = key
        self._ID = key
        self._category = category
        self._name = "{} {}".format(category.value, key) if name is None else name
        self._race = race
        self._ethnicity = ethnicity
        self._gender = gender
        self._setting = setting
        self._reason = reason
        self._birthdate = birthdate
        self._disability = disability

    def get_id(self):
        return self._key

    def set_name(self, value):
        self._name = value

    @staticmethod
    def from_dict(record_dict):
        key = record_dict.get('key')
        category = Category.get_name(record_dict.get('category'))
        race = Race.get_name(record_dict.get('race'))

        return Record(key, category, race=race)

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self._key),
            "ID": "{}".format(self._ID),
            "name": self._name,
            "category": self._category.value,
        }
        if self._category == Category.PARTICIPANT:
            if self._birthdate is not None:
                result['birthdate'] = self._birthdate
            if self._disability is not None:
                result['disability'] = self._disability
            if self._gender != Gender.NONE:
                result['gender'] = self._gender.value
            if self._race != Race.NONE:
                result['race'] = self._race.value

        return result

    def to_json(self):
        return json.dumps(self.to_dict())
