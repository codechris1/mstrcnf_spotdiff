
import os
import sys
import json
import hashlib
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

def compare_arrays(base_array, base_info, new_array, new_info):
    result = []
    row = 0
    elementdic = {}

    elementdic['sn1'] = base_info('sn')
    elementdic['sn2'] = new_info('sn')
    elementdic['pr1'] = base_info('pr')
    elementdic['pr2'] = new_info('pr')
    elementdic['source'] = base_info('sr')
    elementdic['usr1'] = base_info('usr')
    elementdic['usr2'] = new_info('usr')

    base_array_copy = base_array

    for element in new_array:

        found = False
        row = row + 1
        elementdic['row'] = row

        elementdic['setname'] = element['name']
        elementdic['setlevel'] = element['level']
        elementdic['parent1'] = element['parent1']
        elementdic['parent2'] = element['parent2']
        elementdic['val2'] = element['value']

        for target in base_array_copy:
            if element['hashkey'] = target['hashkey']:
                found = True
                elementdic['val1'] = target['value']
                if element['value'] = target['value']:
                    elementdic['diff'] = 0
                else:
                    elementdic['diff'] = 1
                
                base_array_copy.remove(target)
                break
        
        if not found :
            elementdic['val1'] =''
            elementdic['diff'] = 1
        
        result.append(elementdic)
    
    for element in base_array_copy:
        row = row + 1
        elementdic['row'] = row

        elementdic['setname'] = element['name']
        elementdic['setlevel'] = element['level']
        elementdic['parent1'] = element['parent1']
        elementdic['parent2'] = element['parent2']

        elementdic['val1'] = element['value']
        elementdic['val2'] = ''
        elementdic['diff'] = 1

        result.append(elementdic)
    
    return result