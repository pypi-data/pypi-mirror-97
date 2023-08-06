from __future__ import print_function
import getpass
import sys
import re
import json
from loreiosdk.spyglass_script import Spyglass, LoreException

"""
    This is a Sabre Specific script.
    pre-req: having CUST table with Lore Sourceline column 
    
    usage: this command will automap every lore_sourceline column from the CUST Tables to lore_lineno
        stg: 'ws://stg01.getlore.io/storyteller'
        prod: 'wss://ui.getlore.io/storyteller'
    Python 3.xx Compliant
    date: 02/12/2020
    author: clement
"""


WS_URL = 'ws://stg01.getlore.io/storyteller'
DATASET_ID = 'sabre_demo'


def automap():
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
    # Filter Customer Table group
    try:
        res = api.cmd('table', filter='\'{"table_group": "Customer Tables"}\'')
    except LoreException as e:
        print(e)
        sys.exit()
    for tables in res['data']:
        table_id = tables['id']
        res = api.cmd('dimension', table=table_id)
        for col in res['data']:
            col_name = col['name']
            if bool(re.search('Lore SourceLine$', col_name)) and 'automap' not in col:
                col_id = col['id']
                col['automap'] = 'lore_lineno'
                try:
                    col = json.dumps(col)
                    api.cmd('dimension', col_id, put='\'{}\''.format(col))
                    print(col_name + '  --> Done')
                except LoreException as e:
                    print(e)


if __name__ == "__main__":
    automap()
