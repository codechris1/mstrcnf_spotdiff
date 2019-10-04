import json
from collections import OrderedDict

def input_parameters():
    args={}
    input_texts=OrderedDict(
        [
            ("path","Provide the Path Location: "),
            ("server1", "Provide the Hostname for Server 1 : "),
            ("user1", "Provide the User for Server 1 : "),
            ("password1", "Provide the Password for Server 1 : "),
            ("port1", "Provide the Port for Server 1 : "),
            ("project1", "Provide the Project for Server 1 : "),
            ("server2", "Provide the Hostname for Server 2 : "),
            ("user2", "Provide the User for Server 2 : "),
            ("password2", "Provide the Password for Server 2 : "),
            ("port2", "Provide the Port for Server 2 : "),
            ("project2", "Provide the Project for Server 2 : ")
        ]
    )
    for element in input_texts:
        args[element]=raw_input(input_texts[element])
    return args

args = input_parameters()
print args
    
    #args['path']=raw_input('Provide the Path Locaton: ')
    #args['server1']=raw_input('Provide the Hostname for Server 1: ')