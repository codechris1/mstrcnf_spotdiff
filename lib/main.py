import os
import sys
import json
import utility
import copy
from constaint import ServerAttr
from datetime import date
from datetime import time
from datetime import datetime


def main():
    source_project='Project'
    source_server='Server'
    today=datetime.now()
    inputu = utility.pick_config()
    args = inputu[1]
    config_name = inputu[0].replace('.json','')
    

    #Create Project Sources
    utility.create_project_source(args['path'],args['server1'],args['port1'],args['user1'],args['password1'])
    utility.create_project_source(args['path'],args['server2'],args['port2'],args['user2'],args['password2'])

    #Gather Server Configurations
    server_level1 = utility.rf_cmmgr(args['path'], args['server1'], args['user1'], args['password1'], args['port1'], args['project1'], source_server)
    server_level2 = utility.rf_cmmgr(args['path'], args['server2'], args['user2'], args['password2'], args['port2'], args['project2'], source_server)

    #Gather Project Configurations
    project_level1 = utility.rf_cmmgr(args['path'], args['server1'], args['user1'], args['password1'], args['port1'], args['project1'], source_project)
    project_level2 = utility.rf_cmmgr(args['path'], args['server2'], args['user2'], args['password2'], args['port2'], args['project2'], source_project)

    server_info1 = {
    ServerAttr.NAME : args['server1'],
    ServerAttr.PROJECT :  '',
    ServerAttr.USER : args['user1'],
    ServerAttr.SOURCE : source_server
    }

    project_info1 = copy.copy(server_info1)
    project_info1[ServerAttr.SOURCE] = source_project
    project_info1[ServerAttr.PROJECT] = args['project1']

    server_info2 = {
    ServerAttr.NAME : args['server2'],
    ServerAttr.PROJECT :  '',
    ServerAttr.USER : args['user2'],
    ServerAttr.SOURCE : source_server
    }

    project_info2 = copy.copy(server_info2)
    project_info2[ServerAttr.SOURCE] = source_project
    project_info2[ServerAttr.PROJECT] = args['project2']

    compare_result_server = utility.compare_arrays(server_level1, server_info1, server_level2, server_info2)

    compare_result_project = utility.compare_arrays(project_level1, project_info1, project_level2, project_info2)

    utility.save_results(compare_result_server+compare_result_project,'compare_results_' + config_name + today.strftime("_%m-%d-%Y_%H%M%S"))

if __name__ == '__main__':
    main()