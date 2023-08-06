import json
import os

from pybrary.curation.types.release import Release
from pybrary.utils import utils
from pybrary import constants


class Asset:
    def __init__(
            self,
            file,
            id,
            name=None,
            position='auto',
            release=Release.PRIVATE,
            clips=None
    ):
        self._file_ext = utils.get_file_extension(file)
        if not self.is_supported(self._file_ext):
            raise Exception('Asset format {} not supported'.format(self._file_ext))

        if not self.is_media() and clips is not None:
            raise Exception('Cannot add clips for {}. Clips are only supported for media types'.format(self._file_ext))

        self._clips = clips
        self._id = id
        self._file = file
        self._name = utils.get_file_name(file) if name is None else name
        self._position = position
        self._release = release

    def get_id(self):
        return self._id

    def set_name(self, value):
        self._name = value

    def set_release(self, release):
        self._release = release

    @staticmethod
    def from_dict(asset_dict):
        file = asset_dict.get('file')
        id = asset_dict.get('id')
        if file is None:
            raise IOError('You must provide a path to the file. '
                          'Please edit file column for row {}'
                          .format(id))

        name = asset_dict.get('name')
        return Asset(file, id, name=name)

    def to_dict(self, template=False):
        result = {
            "id": self._id,
            "release": self._release.value,
            "position": self._position,
            "name": self._name,
            "file": os.path.abspath(self._file)
        }

        if template and self._clips is None:
            result['clip'] = []
        if not template and self._clips is not None:
            result['clip'] = self._clips

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def is_media(self):
        if self._file_ext in constants.VIDEO_EXTENSIONS \
                or self._file_ext in constants.AUDIO_EXTENSIONS:
            return True
        else:
            return False

    def is_supported(self, file_extension):
        if file_extension is None or len(file_extension) < 1:
            raise Exception('File extension is missing, please provide a file name with a valid extension')

        if file_extension in constants.SUPPORTED_FORMATS.values():
            return True

        return False
