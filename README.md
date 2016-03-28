#CKAN Data Quality

This repository contains scripts that can be used to generte csv files giving information 
about the publishers and the sources of any ckan repository.

## Installation
Create your virtual environment and install the requirements:
```
pip install -r requirements.txt
```
You should be able to use both python2 and python3.

## Usage

The `create_sources.py` script can be run to create the `sources.csv` file.
This file contains all the sources (so all datasets) that are in the given ckan instance.
It is called by running 
```
./create_sources.py <ckan-endpoint>
```

The example data contained here was created by calling:

```
./create_sources.py https://data.qld.gov.au/
```

Similarily the `create_publishers.py` script creates the `publishers.csv` file. 
The example file included here was created by running
```
./create_publishers.py https://data.qld.gov.au/
```
