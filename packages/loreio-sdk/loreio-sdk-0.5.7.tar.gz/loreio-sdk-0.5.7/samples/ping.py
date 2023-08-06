from time import sleep

from loreiosdk.spyglass_script import Spyglass


url = 'wss://ui.getlore.io/storyteller'
user = 'USR'
pwd = 'PWD'


spyglass = Spyglass(url, user, pwd, dataset_id='DS')

print(spyglass.cmd('ping'))

while True:
    sleep(1)
    try:
        print(spyglass.cmd('ping'))
    except:
        pass