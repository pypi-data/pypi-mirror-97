# Python Databrary API Wrapper
This is a Python wrapper around [databrary](https://www.databrary.org) API

## Installation 
Run the following to install:
```bash
pip install pydatabrary
```

## Usage

### Databrary API
```python
from pybrary import Pybrary

# Start a Databrary session
pb = Pybrary.get_instance('USERNAME', 'PASSWORD')
# You need to have permissions to the volume, to interact with it
volume_info = pb.get_volume_info(1)
print(volume_info)
```

### Databrary Curation
#### Generate tamplates

```python
from pybrary import Curation

assets = Curation.generate_assets_list('/PATH/TO/ASSET/FOLDER', '/PATH/TO/OUTPUT/CSV')

# The number of records that you need for your ingest
payload = {
    'participant': 0,
    'pilot': 0,
    'exclusion': 0,
    'condition': 0,
    'group': 0,
    'task': 0,
    'context': 0,
}
records = Curation.generate_records_list(categories=payload, output='/PATH/TO/OUTPUT/CSV')

# Value is the number of containers you wish to generate
containers = Curation.generate_containers_list(value=2, output='/PATH/TO/OUTPUT/CSV')
```

#### Read CSV files
After you edit your CSV files you will have to pass them to ```pybrary``` to validate them and
generate JSON file needed for your ingest

Only containers are required, if you provide assets and records files```pybrary``` will populate
assets and records found in the container fields

Note: ```pybrary``` will ignore duplicate keys, so make sure to have unique ids for your rows
```python
from pybrary import Curation

# You can read your files separately to edit them programmatically 
assets = Curation.read_assets_csv('/PATH/TO/ASSETS/CSV')
records = Curation.read_records_csv('/PATH/TO/RECORDS/CSV')
containers = Curation.read_containers_csv('/PATH/TO/CONTAINERS/CSV')
```
Generate the ingest file
```python
from pybrary import Curation

curation = Curation(
    'Volume',
    '/PATH/TO/CONTAINERS/CSV',
    assets_file='/PATH/TO/ASSETS/CSV',
    records_file='/PATH/TO/RECORDS/CSV'
)
curation.generate_ingest_file('/PATH/TO/JSON/OUTPUT')
```


## Development
Install Locally
```shell
pip instal -e .
```

Build
```shell
python -m build
```

Publish
```shell
twine upload dist/*
```



