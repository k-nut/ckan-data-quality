#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import csv

import requests
import click

def get_organizations(base_url):
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
    data = get_organizations(base_url)
    orgas = []
    for organization in data['result']:
        orgas.append(parse_organization(organization))
    persist_organizations(orgas)


def parse_organization(organization):
    data = {}
    data['id'] = organization.get('name', '')
    data['title'] = organization.get('display_name', '')
    for extra in organization.get('extras', []):
        key = extra.get('key')
        # print(key)
        if key == 'contact-email':
            data['email'] = extra.get('value')
        if key == 'contact-name':
            data['contact'] = extra.get('value')
        if key == 'category':
            data['type'] = extra.get('value')

    return data

def persist_organizations(orgas):
    with open('publishers.csv', 'w') as csvfile:
        fieldnames = ['id', 'title', 'type', 'contact', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for orga in orgas:
            writer.writerow(orga)

if __name__ == "__main__":
    extract_organizations()
