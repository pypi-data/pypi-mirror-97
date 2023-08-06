![pypi](https://img.shields.io/pypi/v/cannerflow-python-client.svg)

# Introduction

This package provides a client interface to query Cannerflow
a distributed SQL engine. It supports Python 2.7, 3.5, 3.6, and pypy.

# Installation

```
$ pip install cannerflow-python-client
```

# Quick Start

## Client
```python
client = cannerflow.client.bootstrap(
    endpoint="http://localhost:3000",
    workspace_id=WORKSPACE_ID,
    headers={
        'X-CANNERFLOW-SECRET': JUPYTER_SECRET,
        'X-CANNERFLOW-WORKSPACE-ID': WORKSPACE_ID
    }
)
queries = client.list_saved_query()
query = client.use_saved_query('region')
raws = query.get_all()
```

# Development
## Setup virtual env

[ref](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```
python3 -m venv env
source env/bin/activate

```

## Install package for test
```
pip install -e .[tests]
```

## Run test with given workspaceId and token

**example**
```
export WORKSPACE_ID="2fae9bf7-a883-4f25-9566-c0d379c44440"
export CSV_FILE="test.csv"
export CANNERFLOW_PERSONAL_ACCESS_TOKEN=Y2xpZW50X2U3MWIxOTIwLWQyYTktNDkyMy05MDdhLWM3MDE4Njk3MmQwNzpjMTI4MzRjNTkxOGI5N2E2ZTBiYzVhN2I3NDllZGRhYg==
python3 -m tests.test_utils
python3 -m tests.test_client
python3 -m tests.test_csv_wrapper
```


## Publish


```sh
# update version in __init__
vim cannerflow/__init__.py
rm -rf dist
python setup.py sdist
twine upload dist/*
```
