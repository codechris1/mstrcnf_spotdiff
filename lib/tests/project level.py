import os
import sys
import json
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

    script = """[Client]
    Client=1
    ConnType=3
    Timeout=5"""
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


command = "LIST ALL PROPERTIES FOR PROJECT CONFIGURATION IN PROJECT '"+project+"';"
validation_str = ["Task(s) execution completed successfully."]
cmdexecutor = cmdmgrExecutor(MSTRPath, server_name, user_name, user_pwd)
execution = cmdexecutor.run_validation(command, validation_str)
'''
print "this is the execution"
if not execution[0]:
        raise Exception('Error on executing ' + command)
'''

format_output={}
row_number=1
source='Project'
for raw in execution[1]:
    #print raw
    raw=raw.replace('\n','')
    row = {}
    row['row_number']=row_number
    if '=' in raw:
        row['type']='value'
        setting=raw.split(' = ')
        row['name']=setting[0]
        row['value']=setting[1]
    else:
        row['type']='parent'
        row['name']=raw
        row['value']=''
    

    row['row_number']=row_number
    row_number=row_number+1
    print row
    format_output.update(row)

#print format_output


