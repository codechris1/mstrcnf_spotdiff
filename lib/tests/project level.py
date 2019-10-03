import os
import sys
import json
import hashlib
from itertools import cycle
from cmdmgr_executor import Executor as cmdmgrExecutor
from cfgwiz_executor import Executor as cfgwizExecutor

def create_script(data_source, server_name, port_number, authentication, user_name, user_pwd, dsn):
    # Authentication method
    auth_lower = authentication.lower()
    auth = 0
    if auth_lower == 'standard':
        auth = 1
    elif auth_lower == 'windows':
        auth = 2
    elif auth_lower == 'anonymous':
        auth = 8
    elif auth_lower == 'ldap':
        auth = 16
    elif auth_lower == 'database':
        auth = 32
    elif auth_lower == 'integrated':
        auth = 128

    script = '''[Client]
    Client=1
    ConnType=3
    Timeout=5'''
    script += '\nDataSource=' + data_source
    script += '\nServerName=' + server_name
    script += '\nPort=' + port_number
    script += '\nAuthentication=' + str(auth)
    if dsn:
        script += '\nDSN=' + dsn
    if user_name and user_pwd:
        script += '\nEncryptPassword=0'
        script += '\nUserName=' + user_name
        script += '\nUserPwd=' + user_pwd

    return script

def create_project_source(MSTRPath,server_name,port,user_name,user_pwd):
        executor = cfgwizExecutor( MSTRPath, True)
        authmethod='standard'
        script = create_script(server_name, server_name, port, authmethod,user_name,user_pwd ,'DSN')
        executor.run_cfgwiz(script)


#MSTRPath = '/opt/mstr/MicroStrategy'
MSTRPath = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
server_name = 'env-165136laiouse1'
user_name = 'Administrator'
user_pwd = 'mYJ80QKa2hbu'
port = '34952'
project = 'MicroStrategy Tutorial'
create_project_source(MSTRPath,server_name,port,user_name,user_pwd)


command = 'LIST ALL PROPERTIES FOR PROJECT CONFIGURATION IN PROJECT "'+project+'";'
#command = 'LIST ALL PROPERTIES FOR SERVER CONFIGURATION;'
validation_str = ['Task(s) execution completed successfully.']
cmdexecutor = cmdmgrExecutor(MSTRPath, server_name, user_name, user_pwd)
execution = cmdexecutor.run_validation(command, validation_str)
'''
print 'this is the execution'
if not execution[0]:
        raise Exception('Error on executing ' + command)
'''

format_output=[]
setting_id=1
source='Project'
running = True
#licycle = cycle(execution[1])
#nextraw = next(licycle)
parent1=''
parent2=''
for raw in execution[1]:
#while running:
    #raw, nextraw = nextraw, next(licycle)
    #print raw
    row = {}
    raw=raw.replace('\n','')
    if '\t' in raw:
        row['level']=raw.count('\t')
    else:
        row['level']=0
    raw=raw.replace('\t','')
    row['setting_id']=setting_id
    if ' = ' in raw:
        row['type']='value'
        setting=raw.split(' = ')
        row['name']=setting[0]
        row['value']=setting[1]
    else:
        row['type']='parent'
        row['name']=raw
        row['value']=''
    row['source']=source
    row['setting_id']=setting_id
    setting_id=setting_id+1
    if row['level']==0 and row['type']=='parent':
        parent1=row['name']
    if row['level']==1 and row['type']=='parent':
        parent2=row['name']
    if row['level']==0 and row['type']=='value':
        row['parent1']=''
        row['parent2']=''
    elif row['level']==1 and row['type']=='value':
        row['parent1']=parent1
        row['parent2']=''
    else:
        row['parent1']=parent1
        row['parent2']=parent2
    if row['level']==2:
        row['location']=row['parent1']+' > '+row['parent2']+' > '+row['name']
        row['rawkey']=row['parent1']+' > '+row['parent2']+' > '+row['name'] + ' = ' + row['value']
    elif row['level']==1:
        row['location']=row['parent1']+' > '+row['name']
        row['rawkey']=row['parent1']+' > '+row['name'] + ' = ' + row['value']
    else:
        row['location']=row['name']
        row['rawkey']=row['name'] + ' = ' + row['value']
    hashedkey=hashlib.md5(row['rawkey'].encode())
    row['hashkey']=hashedkey.hexdigest()
    if row['type']=='value':
        format_output.append(row)
    #print row

#print '\nThe json starts here\n'


#with open('test.json','w+') as jsonfile:
#    json.dump(format_output,jsonfile)

