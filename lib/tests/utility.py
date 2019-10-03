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

def is_valid_string(string_value):
        if "pm" in string_value:
            return False
        if "am" in string_value:
            return False
        if "==================================" in string_value:
            return False
        if "####################################" in string_value:
            return False
        return True

def remove_newline(string_value):
        return string_value.rstrip()

#MSTRPath = '/opt/mstr/MicroStrategy'
MSTRPath = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
server_name = 'env-165137laiouse1'
user_name = 'Administrator'
user_pwd = 'X9pUk9iVsdyu'
port = '34952'

create_project_source(MSTRPath,server_name,port,user_name,user_pwd)


command = "LIST ALL PROPERTIES FOR SERVER CONFIGURATION;"
validation_str = ["Task(s) execution completed successfully."]
cmdexecutor = cmdmgrExecutor(MSTRPath, server_name, user_name, user_pwd)
execution = cmdexecutor.run_validation(command, validation_str)
print "this is the execution"
#print execution

for n in execution[1]:
    if is_valid_string(n):
         print remove_newline(n)
if not execution[0]:
        raise Exception('Error on executing ' + command)
