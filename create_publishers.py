#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is supplied a ckan endpoint api. It creates a `publishers.csv` file that
contains all the publishing organizations and their contact data
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import codecs

import requests
import click

def get_organizations(base_url):
    """
    Makes a request to the ckan api for the given `base_url` and
    returns the response as a dictionary
    """
    extension = "api/3/action/organization_list"
    payload = {'all_fields':True,
               'include_groups': True,
               'include_extras':True
              }
    full_url = base_url + extension
    response = requests.get(full_url, params=payload)
    return response.json()

@click.command()
@click.argument('base_url')
def extract_organizations(base_url):
    """
    The main function.
    """
    data = get_organizations(base_url)
    orgas = [parse_organization(orga) for orga in data['result']]
    persist_organizations(orgas)


def parse_organization(organization):
    """
    Converts `organization` into dicitonary that has standard
    compliant field names
    """
    data = {}
    data['id'] = organization.get('name', '')
    data['title'] = organization.get('display_name', '')
    for extra in organization.get('extras', []):
        key = extra.get('key')
        if key == 'contact-email':
            data['email'] = extra.get('value')
        if key == 'contact-name':
            data['contact'] = extra.get('value')
        if key == 'category':
            data['type'] = extra.get('value')

    return data

def persist_organizations(orgas):
    """
    writes the collected organizations to the `publishers.csv` file
    """
    with codecs.open('publishers.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'type', 'contact', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for orga in orgas:
            writer.writerow(orga)

if __name__ == "__main__":
    extract_organizations()  #pylint: disable=no-value-for-parameter
