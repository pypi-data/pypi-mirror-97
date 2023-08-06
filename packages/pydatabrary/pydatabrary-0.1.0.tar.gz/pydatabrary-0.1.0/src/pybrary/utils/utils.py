import os
import csv
import json
import pandas as pd
from pybrary import constants


def replace_file_extension(file_path, file_format='json'):
    root = get_file_root(file_path)
    file_name = get_file_name_no_extension(file_path)
    return os.path.join(root, "{}{}{}".format(file_name, '.', file_format))


def get_file_extension(file_path):
    file_name, file_extension = os.path.splitext(get_file_name(file_path))
    return file_extension[1:]


def get_file_name_no_extension(file_path):
    file_name, file_extension = os.path.splitext(get_file_name(file_path))
    return file_name


def get_file_root(file_path):
    return os.path.dirname(os.path.abspath(file_path))


def get_file_name(file_path):
    return os.path.basename(file_path)


def get_supported_formats():
    return constants.SUPPORTED_FORMATS.values()


def dump_into_csv(data_list, output, index=False):
    df = pd.read_json(json.dumps(data_list))
    df.to_csv(output, index=index, index_label='id', quoting=csv.QUOTE_ALL)


def dump_into_json(data_list, output):
    with open(output, 'w') as outFile:
        json.dump(data_list, outFile)


def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict('records')
