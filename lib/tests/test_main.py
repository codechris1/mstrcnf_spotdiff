import utility
import json
import os

def save_config(args,config_name):
    with open('conf\\' + config_name + '.json','w+') as jsonfile:
        json.dump(args, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)

def pick_config():
    list_files={}
    fnumber=1
    args={}
    picked=0
    #print('The following configuration files where found :')
    for root, dirs, files in os.walk("conf\\"):
        for filename in files:
            list_files[fnumber]=filename
            fnumber=fnumber+1
    if len(list_files) > 0:
        print('The following configuration files where found: ')
        for f in list_files:
            print(str(f) + ' : ' + list_files[f])
        picked=int(raw_input('Select a file by typing the index : '))
        with open("conf\\"+list_files[picked]) as fparams:
            args=json.load(fparams)
        return list_files[picked],args,True
    return '',args,False
'''
args = utility.input_parameters()
print args
save_config(args,'test1')
save_config(args,'test2')
save_config(args,'test3')
'''
args = pick_config()
print args
#print args[1]