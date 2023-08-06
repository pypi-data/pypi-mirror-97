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
# bootstrap cannerflow client with credentials
client = cannerflow.client.bootstrap(
  endpoint='https://web.default.myname.apps.cannerflow.com',
  workspace_id='444e8753-a4c0-4875-bdc0-834c79061d56',
  token='Y2xpZW50XzA0OTgzODM4LWNhZjktNGNmZi1hNDA4LWFkZDY3ZDc5MjIxNjo2N2YyNGY5OWEzYjFiZTEyZTg2MDI2MmMzNGQzZDRiYQ=='
)

# generate simple tpch query
query = client.gen_query('select * from tpch.tiny.region', data_format='list')
query.wait_for_finish()

# get all data with `get_all()` and data will be list of rows
data = query.get_all()
```

## Learn more
Please learn more from
1. [CannerFlow Official Document](https://flow.cannerdata.com/)
1. [Python Client Document](https://flow.cannerdata.com/docs/integration/development_python)
