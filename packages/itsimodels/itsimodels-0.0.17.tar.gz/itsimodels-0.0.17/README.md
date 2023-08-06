# Model Definitions for Splunk IT Service Intelligence

## Setup Virtualenv

```
python3 -m venv /path/to/new/virtual/environment

source /path/to/new/virtual/environment/bin/activate
```

## Install the Python package

```
pip install --upgrade itsimodels
```

## Building the distribution archive

Install the build dependencies:
```
pip install --upgrade setuptools wheel
```

### Generate the Python package

Run this command to generate the Python distribution archive:
```
make
```

### Upload to the Python Package Index

Install the dependencies required for uploading to the index:

```
pip install --upgrade twine
```

Upload to PyPI:

```
make upload
```
