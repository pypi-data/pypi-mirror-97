#Lore IO python SDK


####Interactive shell:
```bash 
python -m loreio-sdk wss://ui.getlore.io/storyteller
 ```  
More information here : https://loreio.atlassian.net/wiki/spaces/LD/pages/711720969/Spyglass+Interactive+Shell

####Scripting: 
 ```python
from loreiosdk.spyglass_script import Spyglass   

# get your spyglass instance
spyglass_instance = Spyglass('wss://ui.getlore.io/storyteller', 'USERNAME',
'PASSWORD', dataset_id='DATASET_ID')

# cmd will trigger an sync command and will return an JSON object containing the result    
# passing a keyword argument = None is the equivalent of passing --argument without any value in the shell
# result will always be in the following format:
# {'seqno': 0, 'message': 'the message from the b-e', 'data': {"Some json/array": 0}} 
# based the command used, message and/or data can be None  
result = spyglass_instance.cmd("Command Name", "argument1", "argument2", Keyword_arg1=True, arg2=None)

# streaming_cmd will return a generator. 
# Today it is only compatible with the "chart" 
# result will be formatted like 
for result in spyglass_instance.streaming_cmd('chart', 'chart_id', streaming=None):
    print result  

# async_cmd will trigger a none blocking command, allowing you to do something else 
# and if you need the result later, you can use get_result_for_cmd with the seqno
# to get the status ('IN_PROGRESS' or 'DONE') and if done, the result of your command. 
seqno = spyglass_instance.async_cmd("Command Name", "Positional_argument", Keyword_arg=1)
print "Do Something else"
status, result = spyglass_instance.get_result_for_cmd(seqno)

```

  

##Contributors resources 

Build using:
```bash
update version in setup.py and __init__.py

python setup.py sdist bdist_wheel  
```
Publish using: 
```bash
twine upload dist/loreio-sdk-VERSION.tar.gz
```