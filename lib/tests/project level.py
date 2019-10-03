import utility
import json



MSTRPath = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
server_name = 'env-165136laiouse1'
user_name = 'Administrator'
user_pwd = 'mYJ80QKa2hbu'
port = '34952'
project = 'MicroStrategy Tutorial'
utility.create_project_source(MSTRPath,server_name,port,user_name,user_pwd)

project_output=utility.rf_cmmgr(MSTRPath, server_name, user_name, user_pwd, port, project, 'Project')
server_output=utility.rf_cmmgr(MSTRPath, server_name, user_name, user_pwd, port, '', 'Server')

with open('test.json','w+') as jsonfile:
    json.dump(project_output+server_output,jsonfile)