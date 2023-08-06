[![Build Status](http://drone.waylay.io/api/badges/waylayio/waylay-py/status.svg)](http://drone.waylay.io/waylayio/waylay-py)

# waylay-py
Python SDK for the Waylay Platform

## Prerequisites
This package requires a python runtime `3.6` or higher.
For datascience purposes you typically want to prepare a anaconda environment:
```bash
conda create --name my_waylay_env python=3.8
conda activate my_waylay_env
conda install jupyter
pip install waylay-beta # .. or any of the other installation methods below
jupyter notebook 
```

## Installation

### from [Python Package Index](https://pypi.org/project/waylay-beta/)
```bash
pip install waylay-beta
```
### from [this repository](https://github.com/waylayio/waylay-py)
```bash
pip install git+https://github.com/waylayio/waylay-py@v0.1.2
```

### from source
```bash
git clone https://github.com/waylayio/waylay-py
pip install -e ./waylay-py
```
See [Development Manual](doc/dev.md) for more details.

## User Documentation

> `[SaaS]` https://docs.waylay.io/api/sdk/python/<br>
> `[io]` https://docs-io.waylay.io/#/api/sdk/python<br>

## Usage
See [demo notebooks](https://github.com/waylayio/demo-general/tree/master/python-sdk) for usage examples.

## Development
See [Development Manual](doc/dev.md)
