import os
import sys
import json
import hashlib
import copy
from constaint import ServerAttr, SettingAttr, SettingDSAttr
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
        if raw.startswith('<') or raw.startswith('src=\"'):
            continue
        row = {}
        raw=raw.replace('\n','')
        if raw.startswith('\t\t'):
            row[SettingAttr.LEVEL]=2
        elif raw.startswith('\t'):
            row[SettingAttr.LEVEL]=1
        else:
            row[SettingAttr.LEVEL]=0
        raw=raw.replace('\t','')
        row[SettingAttr.ID]=setting_id
        if ' = ' in raw:
            row[SettingAttr.TYPE]='value'
            setting=raw.split(' = ')
            row[SettingAttr.NAME]=setting[0]
            row[SettingAttr.VALUE]=setting[1]
        else:
            row[SettingAttr.TYPE]='parent'
            row[SettingAttr.NAME]=raw
            row[SettingAttr.VALUE]=''

        row[SettingAttr.SOURCE]=source
        row[SettingAttr.ID]=setting_id
        setting_id=setting_id+1
        if row[SettingAttr.LEVEL]==0 and row[SettingAttr.TYPE]=='parent':
            parent1=row[SettingAttr.NAME]
        if row[SettingAttr.LEVEL]==1 and row[SettingAttr.TYPE]=='parent':
            parent2=row[SettingAttr.NAME]
        if row[SettingAttr.LEVEL]==0 and row[SettingAttr.TYPE]=='value':
            row[SettingAttr.PARENTONE]=''
            row[SettingAttr.PARENTTWO]=''
        elif row[SettingAttr.LEVEL]==1 and row[SettingAttr.TYPE]=='value':
            row[SettingAttr.PARENTONE]=parent1
            row[SettingAttr.PARENTTWO]=''
        else:
            row[SettingAttr.PARENTONE]=parent1
            row[SettingAttr.PARENTTWO]=parent2
        if row[SettingAttr.LEVEL]==2:
            row[SettingAttr.LOCATION]=row[SettingAttr.PARENTONE]+' > '+row[SettingAttr.PARENTTWO]+' > '+row[SettingAttr.NAME]
            #row['rawkey']=row['parent1']+' > '+row['parent2']+' > '+row['name'] + ' = ' + row['value']
            row[SettingAttr.RAWKEY]=row[SettingAttr.PARENTONE]+' > '+row[SettingAttr.PARENTTWO]+' > '+row[SettingAttr.NAME]
        elif row[SettingAttr.LEVEL]==1:
            row[SettingAttr.LOCATION]= row[SettingAttr.PARENTONE]+' > '+row[SettingAttr.NAME]
            #row['rawkey']=row['parent1']+' > '+row['name'] + ' = ' + row['value']
            row[SettingAttr.RAWKEY]=row[SettingAttr.PARENTONE]+' > '+row[SettingAttr.NAME]
        else:
            row[SettingAttr.LOCATION]=row[SettingAttr.NAME]
            #row['rawkey']=row['name'] + ' = ' + row['value']
            row[SettingAttr.RAWKEY]=row[SettingAttr.NAME]
        hashedkey=hashlib.md5(row[SettingAttr.RAWKEY].encode())
        row[SettingAttr.HASHKEY]=hashedkey.hexdigest()
        #row['sn']=server_name
        #row['pr']=project
        #row['usr']=user_name
        if row[SettingAttr.TYPE] == 'value':
            format_output.append(row)
    return format_output

def compare_arrays(base_array, base_info, new_array, new_info):
    result = []
    row = 0
    elementdic = {}

    elementdic[SettingDSAttr.SEVERNAMEONE.value] = base_info[ServerAttr.NAME]
    elementdic[SettingDSAttr.SERVERNAMETWO.value] = new_info[ServerAttr.NAME]
    elementdic[SettingDSAttr.PROJECTONE.value] = base_info[ServerAttr.PROJECT]
    elementdic[SettingDSAttr.PROJECTTWO.value] = new_info[ServerAttr.PROJECT]
    elementdic[SettingDSAttr.SOURCE.value] = base_info[ServerAttr.SOURCE]
    elementdic[SettingDSAttr.USERONE.value] = base_info[ServerAttr.USER]
    elementdic[SettingDSAttr.USERTWO.value] = new_info[ServerAttr.USER]

    base_array_copy = copy.copy(base_array)

    for element in new_array:
        found = False
        row = row + 1
        elementdic[SettingDSAttr.ROWID.value] = row
        elementdic[SettingDSAttr.LOCATION.value] = element[SettingAttr.LOCATION]

        elementdic[SettingDSAttr.NAME.value] = element[SettingAttr.NAME]
        elementdic[SettingDSAttr.LEVEL.value] = element[SettingAttr.LEVEL]
        elementdic[SettingDSAttr.PARENTONE.value] = element[SettingAttr.PARENTONE]
        elementdic[SettingDSAttr.PARENTTWO.value] = element[SettingAttr.PARENTTWO]
        elementdic[SettingDSAttr.VALUETWO.value] = element[SettingAttr.VALUE]

        for target in base_array_copy:
            if element[SettingAttr.HASHKEY] == target[SettingAttr.HASHKEY]:
                found = True
                elementdic[SettingDSAttr.VALUEONE.value] = target[SettingAttr.VALUE]
                if element[SettingAttr.VALUE] == target[SettingAttr.VALUE]:
                    elementdic[SettingDSAttr.DIFFERENCE.value] = 0
                else:
                    
                    for target1 in base_array_copy:
                        if element[SettingAttr.VALUE] == target1[SettingAttr.VALUE]:
                            if element[SettingAttr.HASHKEY] == target1[SettingAttr.HASHKEY]:
                                elementdic[SettingDSAttr.DIFFERENCE.value] = 0
                                target = target1
                                break

                    elementdic[SettingDSAttr.DIFFERENCE.value] = 1
                
                base_array_copy.remove(target)
                break
        
        if not found :
            elementdic[SettingDSAttr.VALUEONE.value] =''
            elementdic[SettingDSAttr.DIFFERENCE.value] = 1
        
        result.append(copy.copy(elementdic))
    
    for element in base_array_copy:
        row = row + 1
        elementdic[SettingDSAttr.ROWID.value] = row
        elementdic[SettingDSAttr.LOCATION.value] = element[SettingAttr.LOCATION]

        elementdic[SettingDSAttr.NAME.value] = element[SettingAttr.NAME]
        elementdic[SettingDSAttr.LEVEL.value] = element[SettingAttr.LEVEL]
        elementdic[SettingDSAttr.PARENTONE.value] = element[SettingAttr.PARENTONE]
        elementdic[SettingAttr.PARENTTWO.value] = element[SettingAttr.PARENTTWO]

        elementdic[SettingDSAttr.VALUEONE.value] = element[SettingAttr.VALUE]
        elementdic[SettingDSAttr.VALUETWO.value] = ''
        elementdic[SettingDSAttr.DIFFERENCE.value] = 1

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
            args = input_parameters()
            filename_picked = raw_input('Type a name for your new configuration: ') 
            save_config(args,filename_picked)
    else:
        args = input_parameters()
        filename_picked = raw_input('Type a name for your new configuration: ') 
        save_config(args,filename_picked)
    return filename_picked,args

def save_results(args,config_name):
    with open('results\\' + config_name + '.json','w+') as jsonfile:
        json.dump(args, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)