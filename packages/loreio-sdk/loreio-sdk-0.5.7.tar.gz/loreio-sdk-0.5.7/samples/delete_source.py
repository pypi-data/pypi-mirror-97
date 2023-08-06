from __future__ import print_function

"""
    Delete source command
    pre-req: Having a dataset following a specific template:
         --> all sources are mapped to one or more tables under the "Master Tables"'s group
    usage: this command will unmap column/table all tables under "Master Tables"
        group and then delete all sources from project
        stg: 'ws://stg01.getlore.io/storyteller'
        prod: 'wss://ui.getlore.io/storyteller'
    date: 02/12/2020
    author: clement
"""

import getpass
import json
import sys
from loreiosdk.spyglass_script import Spyglass, LoreException

WS_URL = 'wss://ui.getlore.io/storyteller'
DATASET_ID = 'DATASET'


def delete_source():
    # login
    username = input("Username: ")
    password = getpass.getpass()

    api = Spyglass(WS_URL, username, password)
    print(
        "\n------ connected to " + DATASET_ID + ' on ' + WS_URL + " ------\n")

    # session
    try:
        api.cmd("session", DATASET_ID, no_pool=None)
    except LoreException as e:
        print(e)
        sys.exit()

    # filter Master Tables group
    try:
        resp_table = api.cmd('table',
                             filter='\'{"table_group": "Master Tables"}\'')
    except LoreException as e:
        print(e)
        sys.exit()

    # Safety check
    master_tables = []
    for table in resp_table['data']:
        master_tables.append(table['name'])
    sys.stdout.write("are you sure to unmap  " + str(
        len(master_tables)) + " table(s) from LoreIO: \n\n" +
                     "'" + ', '.join(
        master_tables) + "'" + " \n\n(" + WS_URL + ") ? [y/n]")
    choice = input().lower()
    if choice not in ["y", "yes"]:
        sys.exit()

    # loop over master tables
    try:
        resp = api.cmd('table', filter='\'{"name": "Event"}\'')
    except LoreException as e:
        print(e)

    eventtable_id = resp['data'][0]['id']
    for table in resp_table['data']:
        table_id = table['id']
        # re-define all columns to null map columns
        resp = api.cmd('dimension', filter='\'{"table":"' + table_id + '"}\'')
        # loop over columns
        for col in resp['data']:
            col_id = col['id']
            col['calculation']['args'] = []
            col = json.dumps(col)
            try:
                api.cmd('dimension', col_id, put='\'{}\''.format(col))
            except LoreException as e:
                print(e)

        print('-->' + table['name'])
        # unmap table

        # get event table id

        if 'table_inputs' in table:
            for elem in table['table_inputs']:
                elem['table'] = eventtable_id
        else:
            continue
        table = json.dumps(table)
        try:
            resp = api.cmd('table',
                           table_id,
                           put="'" + table + "'")
        except LoreException as e:
            print(e)

    # delete all sources
    try:
        resp = api.cmd('table', filter='\'{"table_group": "Source Tables"}\'')
    except LoreException as e:
        print(e)

    # Safety check
    source_tables = []
    for table in resp['data']:
        source_tables.append(table['name'])
    sys.stdout.write("do you want to delete " + str(
        len(source_tables)) + " sources tables:\n " +
                     ', '.join(source_tables) + "? [y/n]  \n")
    choice = input().lower()
    if choice not in ["y", "yes"]:
        print('\nDone')
        sys.exit()

    # loop over source tables
    for table in resp['data']:
        table_id = table['id']
        try:
            api.cmd('table', table_id, delete=None)
        except LoreException as e:
            print(e)

        print('-->' + table['name'])

    print("\n\n ALL DONE")


if __name__ == "__main__":
    delete_source()
