#CKAN Data Quality

This repository contains scripts that can be used to generte csv files giving information 
about the publishers and the sources of any ckan repository.

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
