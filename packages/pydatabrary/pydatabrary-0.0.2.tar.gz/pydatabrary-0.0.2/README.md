# Python Databrary API Wrapper
This is a Python wrapper around [databrary](https://www.databrary.org) API

## Installation 
Run the following to install:
```bash
pip install pydatabrary
```

## Usage
```python
from pybrary import Pybrary

# Start a Databrary session
pb = Pybrary.get_instance('USERNAME', 'PASSWORD')
# You need to have permissions to the volume, to interact with it
volume_info = pb.get_volume_info(1)
print(volume_info)
```