import os
import sys
import json
import hashlib
import copy
from collections import OrderedDict
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

def rf_cmmgr(MSTRPath, server_name, user_name, user_pwd, port, project, source):
    MSTRPath=MSTRPath
    server_name=server_name
    user_name=user_name
    user_pwd=user_pwd
    port=port
    project=project
    source=source
    command = ''
    if source=='Project':
        command = 'LIST ALL PROPERTIES FOR PROJECT CONFIGURATION IN PROJECT "' + project + '";'
    else:
        command = 'LIST ALL PROPERTIES FOR SERVER CONFIGURATION;'
    validation_str = ['Task(s) execution completed successfully.']
    cmdexecutor = cmdmgrExecutor(MSTRPath, server_name, user_name, user_pwd)
    execution = cmdexecutor.run_validation(command, validation_str)
    if not execution[0]:
        raise Exception('Error on executing ' + command)
    format_output=[]
    setting_id=1
    parent1=''
    parent2=''
    for raw in execution[1]:
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
            #row['rawkey']=row['parent1']+' > '+row['parent2']+' > '+row['name'] + ' = ' + row['value']
            row['rawkey']=row['parent1']+' > '+row['parent2']+' > '+row['name']
        elif row['level']==1:
            row['location']=row['parent1']+' > '+row['name']
            #row['rawkey']=row['parent1']+' > '+row['name'] + ' = ' + row['value']
            row['rawkey']=row['parent1']+' > '+row['name']
        else:
            row['location']=row['name']
            #row['rawkey']=row['name'] + ' = ' + row['value']
            row['rawkey']=row['name']
        hashedkey=hashlib.md5(row['rawkey'].encode())
        row['hashkey']=hashedkey.hexdigest()
        row['sn']=server_name
        row['pr']=project
        row['usr']=user_name
        if row['type']=='value':
            format_output.append(row)
    return format_output

def compare_arrays(base_array, base_info, new_array, new_info):
    result = []
    row = 0
    elementdic = {}

    elementdic['sn1'] = base_info['sn']
    elementdic['sn2'] = new_info['sn']
    elementdic['pr1'] = base_info['pr']
    elementdic['pr2'] = new_info['pr']
    elementdic['source'] = base_info['sr']
    elementdic['usr1'] = base_info['usr']
    elementdic['usr2'] = new_info['usr']

    base_array_copy = copy.copy(base_array)

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
            if element['hashkey'] == target['hashkey']:
                found = True
                elementdic['val1'] = target['value']
                if element['value'] == target['value']:
                    elementdic['diff'] = 0
                else:
                    elementdic['diff'] = 1
                
                base_array_copy.remove(target)
                break
        
        if not found :
            elementdic['val1'] =''
            elementdic['diff'] = 1
        
        result.append(copy.copy(elementdic))
    
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

        result.append(copy.copy(elementdic))

    return result

def input_parameters():
    args={}
    input_texts=OrderedDict(
        [
            ("path","Provide the Path where MicroStrategy is installed (Usually C:\\Program Files (x86)\\Common Files\\MicroStrategy\\) : "),
            ("server1", "Provide the Hostname for Server 1 : "),
            ("user1", "Provide the User for Server 1 : "),
            ("password1", "Provide the Password for Server 1 : "),
            ("port1", "Provide the Port for Server 1 (Usually 34952) : "),
            ("project1", "Provide the Project for Server 1 : "),
            ("server2", "Provide the Hostname for Server 2 : "),
            ("user2", "Provide the User for Server 2 : "),
            ("password2", "Provide the Password for Server 2 : "),
            ("port2", "Provide the Port for Server 2 (Usually 34952) : "),
            ("project2", "Provide the Project for Server 2 : ")
        ]
    )
    for element in input_texts:
        args[element]=raw_input(input_texts[element])
        if element=="path" and args[element] == "":
            args[element] = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
        elif (element=="port1" or element=="port2") and args[element] == "":
            args[element] = "34952"
    return args

def save_config(args,config_name):
    with open('conf\\' + config_name + '.json','w+') as jsonfile:
        json.dump(args, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)

def pick_config():
    list_files={}
    fnumber=1
    args={}
    picked=0
    filename_picked=''
    #print('The following configuration files where found :')
    for root, dirs, files in os.walk("conf\\"):
        for filename in files:
            list_files[fnumber]=filename
            fnumber=fnumber+1
    if len(list_files) > 0:
        print('The following configuration files were found: ')
        for f in list_files:
            print(str(f) + ' : ' + list_files[f])
        try:
            picked=int(raw_input('Select a file by typing the index (If you wish to create a new configuration, hit enter): '))
            with open("conf\\"+list_files[picked]) as fparams:
                args=json.load(fparams)
            filename_picked=list_files[picked]
        except:
            args = utility.input_parameters()
            filename_picked = raw_input('Type a name for your new configuration: ') 
            save_config(args,filename_picked)
    else:
        args = utility.input_parameters()
        filename_picked = raw_input('Type a name for your new configuration: ') 
        save_config(args,filename_picked)
    return filename_picked,args