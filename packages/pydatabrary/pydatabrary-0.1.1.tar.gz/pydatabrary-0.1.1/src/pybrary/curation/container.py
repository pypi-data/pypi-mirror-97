import json
from pybrary.curation.types.release import Release


class Container:
    def __init__(
            self,
            key,
            name=None,
            date=None,
            top=False,
            release=Release.PRIVATE,
            assets=[],
            records=[],
    ):
        self._key = key
        self._top = top
        self._name = "Container {}".format(key) if name is None else name
        self._assets = assets
        self._records = records
        self._release = release
        self._date = date

    def get_assets(self):
        return self._assets

    def get_records(self):
        return self._records

    def set_name(self, value):
        self._name = value

    def set_release(self, release):
        self._release = release

    def add_asset(self, asset_id):
        self._assets.append(asset_id)

    def add_record(self, record_id):
        self._assets.append(record_id)

    @staticmethod
    def from_dict(container_dict):
        key = container_dict.get('key')
        name = container_dict.get('name')
        assets = json.loads(container_dict.get('assets'))
        records = json.loads(container_dict.get('records'))
        release = Release[container_dict.get('release')]
        top = container_dict.get('top')
        return Container(
            key,
            name=name,
            release=release,
            top=top,
            assets=assets,
            records=records
        )

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self._key),
            "top": self._top,
            "name": self._name,
            "release": self._release.value,
        }

        if template:
            result['assets'] = []
            result['records'] = []
        else:
            if len(self._assets) > 0:
                result['assets'] = self._assets
            if len(self._records) > 0:
                result['records'] = self._records

        if self._date is not None:
            result['date'] = self._date

        return result

    def to_json(self):
        return json.dumps(self.to_dict())
