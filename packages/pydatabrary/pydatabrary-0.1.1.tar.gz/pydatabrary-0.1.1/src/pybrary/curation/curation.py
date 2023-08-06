import os
import json
import warnings

from jsonschema import validate, ValidationError
from pybrary import constants
from pybrary.curation.asset import Asset

from pybrary.utils import utils
from pybrary.curation.container import Container
from pybrary.curation.record import Record
from pybrary.curation.types.category import Category


class Curation:
    def __init__(self, volume_name, containers_file, assets_file=None, records_file=None):
        if volume_name is None:
            raise AttributeError('You must provide a valid volume name.')
        self._volume_name = volume_name
        if containers_file is None:
            raise AttributeError('Containers file is required')

        if assets_file is None:
            warnings.warn('Assets found in the containers file will be ignored. PLease provide an assets file')
        else:
            self._assets = Curation.read_assets_csv(assets_file)

        if records_file is None:
            warnings.warn('Records found in the containers file will be ignored. PLease provide a records file')
        else:
            self._records = Curation.read_records_csv(records_file)

        self._containers = Curation.read_containers_csv(containers_file)

    def add_assets(self, file_path):
        self._assets = Curation.read_assets_csv(file_path)

    def add_records(self, file_path):
        self._records = Curation.read_records_csv(file_path)

    def _ignore_assets(self):
        return self._assets is None

    def _ignore_records(self):
        return self._records is None

    def _find_asset(self, asset_id):
        if self._ignore_assets():
            return None

        for asset in self._assets:
            if asset.get_id() == asset_id:
                return asset

        return None

    def _find_record(self, record_id):
        if self._ignore_assets():
            return None

        for record in self._records:
            if record.get_id() == record_id:
                return record

        return None

    def generate_ingest_file(self, output):
        if output is None:
            raise IOError('Please provide an output')
        if utils.get_file_extension(output) != 'json':
            output = utils.replace_file_extension(output)
            warnings.warn('Ingest files must be in JSON format, ingest file will be saved in {}'
                          .format(output))
        result = {
            "name": self._volume_name,
            "containers": []
        }

        for container in self._containers:
            container_dict = container.to_dict()
            asset_ids = container.get_assets()
            container_assets = []
            for asset_id in asset_ids:
                asset = self._find_asset(asset_id)
                container_assets.append(asset.to_dict())

            container_dict['assets'] = container_assets

            record_ids = container.get_records()
            container_records = []
            for record_id in record_ids:
                record = self._find_record(record_id)
                container_records.append(record.to_dict())

            container_dict['records'] = container_records

            result.get('containers').append(container_dict)
        with open(constants.VOLUME_SCHEMA_FILE) as f:
            schema = json.loads(f.read())
        try:
            validate(result, schema)
        except ValidationError as e:
            raise Exception('Did not pass validation against volume.json schema - Errors: {}'.format(e))

        utils.dump_into_json(result, output)
        return result

    @staticmethod
    def generate_assets_list(folder, output=None):
        """
        Find all supported files in a folder (recursively) adds clips for video files.
        return the following structure
            [
                {
                    "release": null,
                    "position": "auto",
                    "name": "FILE_NAME,
                    "file": "FILE_PATH_IN_DATABRARY_STAGING_FOLDER"
                }
            ]
        :param output: dump assets list into a csv file
        :param folder: Folder path where to lookup for assets
        :return: a List of dict with supported assets found in folder
        """
        if not os.path.isdir(folder):
            raise IOError('{} is not a directory'.format(folder))

        print('Parsing {}'.format(os.path.abspath(folder)))
        assets = []
        for root, dirs, files in os.walk(folder):
            for idx, file in enumerate(files):
                try:
                    file_path = os.path.join(root, file)
                    assets.append(Asset(file_path, id=idx))
                except Exception as e:
                    warnings.warn('Error in file {} - '.format(file, e))

        if output is not None:
            Curation.dump_into_csv(assets, output, template=True)
            print('Assets printed in {}'.format(os.path.abspath(output)))

        return assets

    @staticmethod
    def generate_records_list(categories=None, output=None):
        records = []
        idx = 0

        for category, value in categories.items():
            if not Category.has_value(category):
                warnings.warn('Category {} is not valid, it will be ignored'.format(category))
                continue

            if int(value) < 1:
                warnings.warn('The value {} for {} is not valid, it must be > 0'.format(value, category))
                continue

            for i in range(value):
                records.append(
                    Record(
                        category=Category.get_name(category),
                        key=idx,
                    )
                )
                idx = idx + 1

        if output is not None:
            Curation.dump_into_csv(records, output, template=True)
            print('Records printed in {}'.format(os.path.abspath(output)))

        return records

    @staticmethod
    def generate_containers_list(value=1, output=None):
        if int(value) < 1:
            raise Exception('The value {} is not valid, it must be > 0'.format(value))

        containers = []
        for i in range(value):
            containers.append(Container(key="{}".format(i)))

        if output is not None:
            Curation.dump_into_csv(containers, output, template=True)
            print('Containers printed in {}'.format(os.path.abspath(output)))

        return containers

    @staticmethod
    def dump_into_csv(data_list, output, template=False):
        result = []
        for data in data_list:
            try:
                result.append(data.to_dict(template=template))
            except Exception as e:
                print('Error {}'.format(e))
        utils.dump_into_csv(result, output)

    @staticmethod
    def read_records_csv(file_path):
        records_list = utils.read_csv(file_path)
        records = []
        ids = {}
        for record_dict in records_list:
            id = record_dict.get('key')
            if id in ids:
                warnings.warn('Found duplicate key {} in {}, the record {} will be ignored'
                              .format(id, file_path, record_dict.get('name')))
                continue
            ids[id] = None
            record = Record.from_dict(record_dict)
            records.append(record)
        return records

    @staticmethod
    def read_assets_csv(file_path):
        assets_list = utils.read_csv(file_path)
        assets = []
        ids = {}
        for asset_dict in assets_list:
            id = asset_dict.get('id')
            if id in ids:
                warnings.warn('Found duplicate id {} in {}, the asset {} will be ignored'
                              .format(id, file_path, asset_dict.get('name')))
                continue
            ids[id] = None
            asset = Asset.from_dict(asset_dict)
            assets.append(asset)
        return assets

    @staticmethod
    def read_containers_csv(file_path):
        containers_list = utils.read_csv(file_path)
        containers = []
        ids = {}
        for container_dict in containers_list:
            id = container_dict.get('key')
            if id in ids:
                warnings.warn('Found duplicate key {} in {}, the container {} will be ignored'
                              .format(id, file_path, container_dict.get('name')))
                continue
            ids[id] = None
            container = Container.from_dict(container_dict)
            containers.append(container)
        return containers

    @staticmethod
    def generate_sql_query(source, target):
        """
        Generate Databrary DB query that
        :param source: Original Volume ID
        :param target: Target Volume ID
        :return:
        """
        return "COPY (select 'mkdir -p /nyu/stage/reda/' || '" + str(target) + "' || '/' || '" + str(target)
        + "' || sa.container || ' && ' || E'cp \"/nyu/store/' || substr(cast(sha1 as varchar(80)), 3, 2) || '/' || right(cast(sha1 as varchar(80)), -4) || '" "/nyu/stage/reda/' || '"
        + str(target) + "' || '/' || '" + str(target)
        + "' || container || '/' || CASE WHEN a.name LIKE '%.___' IS FALSE THEN a.name || '.' || f.extension[1] ELSE a.name END || E'\"' from slot_asset sa inner join asset a on sa.asset = a.id inner join format f on a.format = f.id where a.volume = "
        + str(source) + ") TO '/tmp/volume_" + str(target) + ".sh';"
