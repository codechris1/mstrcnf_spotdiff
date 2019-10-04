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
    filename_picked=''
    #print('The following configuration files where found :')
    for root, dirs, files in os.walk("conf\\"):
        for filename in files:
            list_files[fnumber]=filename
            fnumber=fnumber+1
    if len(list_files) > 0:
        print('The following configuration files where found: ')
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

args = pick_config()
print args
#print args[1]