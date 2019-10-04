import os
import sys
import json
import utility
from constaint import ServerAttr
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
server_name = 'env-165136-tcp.customer.cloud.microstrategy.com'
user_name = 'Administrator'
user_pwd = 'mYJ80QKa2hbu'
port = '34952'

MSTRPathB = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
server_nameB = 'env-165137-tcp.customer.cloud.microstrategy.com'
user_nameB = 'Administrator'
user_pwdB = 'X9pUk9iVsdyu'
portB = '34952'

create_project_source(MSTRPath,server_name,port,user_name,user_pwd)
create_project_source(MSTRPathB,server_nameB,portB,user_nameB,user_pwdB)




server_output = utility.rf_cmmgr(MSTRPath,server_name, user_name, user_pwd, port, '', 'Server')
server_info = {
    ServerAttr.NAME :'serverA',
    ServerAttr.PROJECT :  '',
    ServerAttr.USER : 'test',
    ServerAttr.SOURCE : 'Server'
}

server_outputB = utility.rf_cmmgr(MSTRPathB,server_nameB, user_nameB, user_pwdB, portB, '', 'Server')
server_infoB = {
    ServerAttr.NAME :'serverB',
    ServerAttr.PROJECT :  '',
    ServerAttr.USER : 'test',
    ServerAttr.SOURCE : 'Server'
}

compare_result = utility.compare_arrays(server_output, server_info, server_outputB, server_infoB)
with open('test.json','w+') as jsonfile:
    json.dump(compare_result,jsonfile)
