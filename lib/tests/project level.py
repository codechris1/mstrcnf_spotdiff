import utility
import json



MSTRPath = 'C:\\Program Files (x86)\\Common Files\\MicroStrategy\\'
#server_name = ''
server_name = ''
user_name = ''
user_pwd = ''
port = '34952'
project = ''

utility.create_project_source(MSTRPath,server_name,port,user_name,user_pwd)

project_output=utility.rf_cmmgr(MSTRPath, server_name, user_name, user_pwd, port, project, 'Project')
#server_output=utility.rf_cmmgr(MSTRPath, server_name, user_name, user_pwd, port, '', 'Server')

print project_output
#print server_output
#with open('results\\test.json','w+') as jsonfile:
#    json.dump(project_output+server_output,jsonfile)
