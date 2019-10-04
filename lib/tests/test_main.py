import utility
import json

def save_config(args,config_name):
    with open('conf\\' + config_name + '.json','w+') as jsonfile:
        json.dump(args, jsonfile, indent=4, separators=(',', ': '), sort_keys=True)


args = utility.input_parameters()
print args
save_config(args,'test1')
