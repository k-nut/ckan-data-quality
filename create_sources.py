#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script can be called with the base url for a ckan instance.
It creates a csv file called sources.csv that contains all available datasets
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import logging
import sys
import codecs

import requests
import click

logging.basicConfig(level=logging.DEBUG)

def get_data(base_url):
    """
    loads the data from the api
    """
    extension = "api/3/action/package_search"
    full_url = base_url + extension
    response = requests.get(full_url)
    if response.status_code == 404:
        logging.warning("%s not found. Exiting", full_url)
        sys.exit(1)
    data = response.json()
    count = data['result']['count']
    logging.info("Total datasets: %i", count)
    all_data = []
    for start in range(0, count, 500):
        all_data += get_results(full_url, start)
    return all_data


def get_results(url, start):
    """
    gets 500 results from the api starting at offset start
    """
    payload = {'rows': 500,
               'start': start
              }
    response = requests.get(url, params=payload)
    data = response.json()
    return data['result']['results']


@click.command()
@click.argument('base_url')
def main(base_url):
    """
    the main function
    """
    results = get_data(base_url)
    sources = []
    for result in results:
        sources += extract_data(result)
    persist_organizations(sources)


def extract_data(datum):
    """
    extract all sources for one result
    """
    resources = []
    import json
    for resource in datum.get('resources', {}):
        new_resource = {}
        try:
            new_resource['publisher_id'] = datum.get('organization', {}).get('name')
        # Not sure why but sometimes this seems to create a None object
        # for which we get an AttributeError when trying to call `get` on it
        except AttributeError:
            new_resource['publisher_id'] = None

        new_resource['id'] = resource.get('id')
        new_resource['format'] = resource.get('format')
        new_resource['data'] = resource.get('url')
        new_resource['last_modified'] = resource.get('last_modified')

        title = datum.get('title', '')
        name = resource.get('name', '')
        new_resource['title'] = ' / '.join(string for string in [title, name] if string)

        resources.append(new_resource)

    return resources

def persist_organizations(sources):
    """
    writes the data to file
    """
    with codecs.open('sources.csv', 'w', encoding="utf8") as csvfile:
        fieldnames = ['id', 'publisher_id', 'title', 'data', 'format', 'last_modified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for source in sources:
            writer.writerow(source)

if __name__ == "__main__":
    main()  #pylint: disable=no-value-for-parameter
