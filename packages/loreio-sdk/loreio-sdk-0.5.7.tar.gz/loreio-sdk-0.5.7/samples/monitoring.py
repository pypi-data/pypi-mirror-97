import time

from loreiosdk.spyglass_script import Spyglass

WS_URL = 'wss://ui.getlore.io/storyteller'
USER = 'USER'
PWD = 'PWD'
DATASET = 'DS'

spyglass = Spyglass(WS_URL, USER, PWD, dataset_id=DATASET)

tables = ['@TABLE_NAME']

for table in tables:
    results = spyglass.cmd('aql',
        ''' 'select count(*) from "{table}" where ingestion_date = \\'{date}\\'' '''
                           .format(table=table,
                                        date=time.strftime("%Y-%m-%d")),
        json=None)
    assert results['data']['series'][0]['data'][0][
               'count'] > 0, "check failed for table : {} ".format(table)
