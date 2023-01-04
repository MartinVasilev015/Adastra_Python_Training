'''
-Refactor the code into several functions or class methods to bring down the cognitive complexity.
'''
import os 
import json 
import hcl 

cfn = [".json", ".template", ".yaml", ".yml"] 
tf  = ["tf"] 

def check_what_file_ends_with(file):
    if file.endswith(tuple(cfn)):
        return 'cfn'
    elif file.endswith(tuple(tf)):
        return 'tf'
    return 'unknown'

def get_data(root, file, file_extention):
    data = ""
    with open(os.path.join(root, file), 'r') as fin: 
        try:
            match file_extention:
                case 'cfn':
                    file = fin.read()
                    if "AWSTemplateFormatVersion" in file:
                        data = json.dumps(file) 
                case 'tf': 
                    obj = hcl.load(fin) 
                    data = json.dumps(obj) 
                case _:
                    data = "Nothing found"
        except ValueError as e: 
            raise SystemExit(e)
    return(data)

def file_handler(dir): 
    for root, dirs, files in os.walk(dir):                          # +1                   
        for file in files:                                          # +2 (nesting 1)
            file_extention = check_what_file_ends_with(file)
            data = get_data(root, file, file_extention)
            print(data)
    return data                                                     # total complexity = 3