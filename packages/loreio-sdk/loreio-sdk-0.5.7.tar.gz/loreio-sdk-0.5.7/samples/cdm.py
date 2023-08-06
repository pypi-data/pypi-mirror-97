import base64
import json
from copy import deepcopy

import requests

from loreiosdk.spyglass_script import Spyglass, LoreException

WS_URL = 'wss://ui.getlore.io/storyteller'
user = 'USR'
pwd = 'PWD'
DATASET_ID = 'DS'

github_user = 'GITHUB_USER'
github_pwd = 'GITHUB_PWD'

spyglass = Spyglass(WS_URL, user, pwd, DATASET_ID)


def get_table_and_columns(file_url):
    r = requests.get(file_url, auth=(github_user, github_pwd))
    model = r.json()
    content = json.loads(base64.b64decode(model[u'content']))
    columns = content[u'definitions'][0][u'hasAttributes'][0][
        u'attributeGroupReference'][u'members']

    return columns


def get_tables_for_entity(entity):
    tables = []
    if entity == 'Core':
        url = 'https://api.github.com/repos/microsoft/CDM/contents/schemaDocuments/core/applicationCommon'
    elif entity == 'marketing':
        url = 'https://api.github.com/repos/microsoft/CDM/contents/schemaDocuments/core/applicationCommon/foundationCommon/crmCommon/solutions/marketing'
    else:
        url = 'https://api.github.com/repos/microsoft/CDM/contents/schemaDocuments/core/applicationCommon/foundationCommon/crmCommon/accelerators/' + entity

    r = requests.get(url, auth=(github_user, github_pwd))
    links = [x['_links']['git'] for x in r.json() if
             'type' in x and x['type'] == 'dir']
    for link in links:
        r = requests.get(link, auth=(github_user, github_pwd))
        # grab all the files that are of v1.0
        files = [x for x in r.json()['tree'] if
                 '1.0' in x['path']]
        for file_ in files:
            try:
                print("fetching {}".format(file_['path'].split('.')[0]))
                columns = get_table_and_columns(file_['url'])
                tables.append({"table_name": file_['path'].split('.')[0],
                               "columns": columns})
            except Exception as e:
                print("could not get data for table : {}".format(
                    file_['path'].split('.')[0]))
    return tables


LORE_TABLE_TEMPLATE = {
    "read_only": False,
    "hidden": False,
    "model_status": "requested",
    "description": "",
    "table_type": "template_table",
    "edited_by_staff": True,
    "labels": {
    },
    "num_ready_dims": 0,
    #################### Table group
    "table_group": "FILL_THIS !",
    "_disabled": False,
    "dataset_id": DATASET_ID,
    "name": "FILL_THIS !"
}

LORE_COLUMN_TEMPLATE = {
    "model_status": "requested",
    "format_blacklist": [
    ],
    "calculation": {
        "wrappers": [
        ],
        "_partition": None,
        "_order": None,
        "_filters": [
        ],
        "is_array": None,
        "args": [
        ],
        "tablename": None,  # To update
        "_num": None,
        "force_null": False,
        "func": "coalesce",
        "_dynamic_args": None,
        "blackbox": False,
        "type": "Advanced",
        "_max_iterations": None
    },
    "labels": {
    },
    "edited_by_staff": True,
    "entity": None,
    "_ui": {
    },
    "owner": "maurin",
    "table": None,  # To update
    "dataset_id": DATASET_ID,
    "dim_status": "published",
    "read_only": False,
    "group": None,
    "namespace": "Local",
    "values_limit": 1000,
    "_disabled": False,
    "hidden": False,
    "type": "Dimension",
    "status": "green",
    "edited_by": "maurin",
    "description": "",
    "data_type": "string",
    "name": None,  # To update
    "dimension_type": "Dimension",
    "formats": [
    ]
}


def get_or_create_object_in_lore(type, lore_object):
    object_dump = json.dumps(lore_object).replace('\'', '\"')
    try:
        obj_cmd = spyglass.cmd(type, filter='\'{}\''.format(object_dump))
        return obj_cmd['data'][0], "GET"
    except Exception as e:
        return spyglass.cmd(type,
                            put='\'{}\''.format(object_dump))['data'], "CREATE"


def create_objects_in_lore(entity, tables):
    def _create_table_cdm(table):
        print('creating table {}'.format(table['table_name']))
        table_lore_object = LORE_TABLE_TEMPLATE
        table_name = entity + ' - ' + table['table_name']
        table_lore_object['name'] = table_name
        table_lore_object['table_group'] = 'CDM - ' + entity

        table_cmd, VERB = get_or_create_object_in_lore('table',
                                                       table_lore_object)
        table_id = table_cmd['id']

        if VERB == 'GET':
            # if table already exists just skip it
            print "Skipping table"
            return

        for col in table['columns']:
            if type(col) != dict:
                continue
            col_name = '@{}.{}'.format(table_lore_object['name'], col['name'])
            column_lore_object = deepcopy(LORE_COLUMN_TEMPLATE)
            column_lore_object['name'] = col_name
            column_lore_object['table'] = table_id
            column_lore_object['calculation']['tablename'] = table_name
            column_lore_object['description'] = col[
                'description'] if 'description' in col else ""
            object_dump = json.dumps(column_lore_object).replace('\'', '\"')
            spyglass.async_cmd('dimension', put='\'{}\''.format(object_dump))

    def _create_validation_table_cds(table):
        print('creating validation table {}'.format(table['table_name']))
        table_lore_object = LORE_TABLE_TEMPLATE
        table_name = entity + ' - ' + table['table_name'] + ' - Validation'
        table_lore_object['name'] = table_name
        table_lore_object['table_group'] = 'CDS - ' + entity
        table_cmd, VERB = get_or_create_object_in_lore('table',
                                                       table_lore_object)
        table_id = table_cmd['id']
        if VERB == 'GET':
            # if table already exists just skip it
            print "Skipping table"
            return
        for col in table['columns']:
            if type(col) != dict:
                continue
            col_name = '@{}.{}-IsValid'.format(table_lore_object['name'],
                                               col['name'])
            column_lore_object = deepcopy(LORE_COLUMN_TEMPLATE)
            column_lore_object['name'] = col_name
            column_lore_object['table'] = table_id
            column_lore_object['calculation']['tablename'] = table_name
            column_lore_object['description'] = col[
                'description'] if 'description' in col else ""
            column_lore_object['data_type'] = 'boolean'
            column_lore_object['calculation']['_data_type'] = 'boolean'
            column_lore_object['calculation']['func'] = 'sql'
            column_lore_object['calculation']["_sql"] = "Not Implemented"
            object_dump = json.dumps(column_lore_object).replace('\'', '\"')
            spyglass.async_cmd('dimension', put='\'{}\''.format(object_dump))

    def _create_table_cdr(table):
        def _get_input_column(col, table_id, table_name):
            col_name = '@{}.{}-INPUT'.format(table_lore_object['name'],
                                             col['name'])
            column_lore_object = deepcopy(LORE_COLUMN_TEMPLATE)
            column_lore_object['name'] = col_name
            column_lore_object['table'] = table_id
            column_lore_object['calculation']['tablename'] = table_name
            column_lore_object['description'] = "INPUT"
            return column_lore_object

        def _get_output_column(col, lore_input_col, table_id, table_name):
            col_name = '@{}.{}-OUTPUT'.format(table_lore_object['name'],
                                              col['name'])
            column_lore_object = deepcopy(LORE_COLUMN_TEMPLATE)
            column_lore_object['name'] = col_name
            column_lore_object['table'] = table_id
            column_lore_object['calculation']['tablename'] = table_name
            column_lore_object['description'] = "OUTPUT"
            column_lore_object['calculation']['args'].append(
                lore_input_col['id'])
            return column_lore_object

        print('creating CDR table {}'.format(table['table_name']))
        table_lore_object = deepcopy(LORE_TABLE_TEMPLATE)
        table_name = entity + ' - ' + table['table_name'] + ' - Rule'
        table_lore_object['name'] = table_name
        table_lore_object['table_group'] = 'CDR - ' + entity

        table_cmd, VERB = get_or_create_object_in_lore('table',
                                                       table_lore_object)
        table_id = table_cmd['id']
        if VERB == 'GET':
            # if table already exists just skip it
            print "Skipping table"
            return

        for col in table['columns']:
            if type(col) != dict:
                continue
            input_col = _get_input_column(col, table_id, table_name)
            input_col_lore, VERB = get_or_create_object_in_lore('dimension',
                                                                input_col)
            output_col = _get_output_column(col, input_col_lore, table_id,
                                            table_name)
            object_dump = json.dumps(output_col).replace('\'', '\"')
            spyglass.async_cmd('dimension',
                               put='\'{}\''.format(object_dump))

    for table in tables:
        _create_table_cdm(table)
        _create_validation_table_cds(table)
        _create_table_cdr(table)


#
# for entity in ["healthCare", "nonProfit", "financialServices", "education"]:
#     print("<><><><><>{}<><><><<>".format(entity))
#     tables = get_tables_for_entity(entity)
#     create_objects_in_lore(entity, tables)


# TODO add sales, marketing

# for entity in ["ApplicationCommon"]:
#     print("<><><><><>{}<><><><<>".format(entity))
#     tables = get_tables_for_entity("Core")
#     create_objects_in_lore("Core", tables)

for entity in ["marketing"]:
    print("<><><><><>{}<><><><<>".format(entity))
    tables = get_tables_for_entity(entity)
    create_objects_in_lore(entity, tables)
