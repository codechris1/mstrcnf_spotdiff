import os
import sys
import json
import utility

def main():
    args = utility.pick_config()[1]

    #Create Project Sources
    utility.create_project_source(args['path'],args['server1'],args['port1'],args['user1'],args['password1'])
    utility.create_project_source(args['path'],args['server2'],args['port2'],args['user2'],args['password2'])

    #Gather Server Configurations
    server_level1 = utility.rf_cmmgr(args['path'], args['server1'], args['user1'], args['password1'], args['port1'], args['project1'], 'Server')
    server_level2 = utility.rf_cmmgr(args['path'], args['server2'], args['user2'], args['password2'], args['port2'], args['project2'], 'Server')

    #Gather Project Configurations
    project_level1 = utility.rf_cmmgr(args['path'], args['server1'], args['user1'], args['password1'], args['port1'], args['project1'], 'Project')
    project_level2 = utility.rf_cmmgr(args['path'], args['server2'], args['user2'], args['password2'], args['port2'], args['project2'], 'Project')

    
 


if __name__ == '__main__':
    main()