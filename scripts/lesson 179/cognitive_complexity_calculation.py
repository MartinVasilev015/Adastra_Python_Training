'''
-Calculate the cognitive complexity of the function
'''
import os 
import json 
import hcl 

cfn = [".json", ".template", ".yaml", ".yml"] 
tf  = ["tf"] 

def file_handler(dir): 
    for root, dirs, files in os.walk(dir):                                      # +1
        for file in files:                                                      # +2 (nesting = 1)
            if file.endswith(tuple(cfn)):                                       # +3 (nesting = 2)
                with open(os.path.join(root, file), 'r') as fin: 
                    try: 
                        file = fin.read() 
                        if "AWSTemplateFormatVersion" in file:                  # +5 (nesting = 4)         
                            data = json.dumps(file) 
                            print(data) 
                    except ValueError as e:                                     # +3 (nesting = 2)
                        raise SystemExit(e) 

            elif file.endswith(tuple(tf)):                                      # +1
                with open(os.path.join(root, file), 'r') as file: 
                    try: 
                        obj  = hcl.load(file) 
                        data = json.dumps(obj) 
                        print(data) 
                    except ValueError as e:                                     # +3 (nesting = 2)
                        raise SystemExit(e) 
    return data   								# total complexity = 18

#-----------------------------------------with the cognitive_complexity package---------------------------------------
>pip install cognitive_complexity


import ast
import os
import json  

cfn = [".json", ".template", ".yaml", ".yml"] 
tf  = ["tf"] 

script = """
def file_handler(dir): 
    for root, dirs, files in os.walk(dir):                                      # +1
        for file in files:                                                      # +2 (nesting = 1)
            if file.endswith(tuple(cfn)):                                       # +3 (nesting = 2)
                with open(os.path.join(root, file), 'r') as fin: 
                    try: 
                        file = fin.read() 
                        if "AWSTemplateFormatVersion" in file:                  # +4 (nesting = 3)         
                            data = json.dumps(file) 
                            print(data) 
                    except ValueError as e:                                     # +4 (nesting = 2)
                        raise SystemExit(e) 

            elif file.endswith(tuple(tf)):                                      # +1
                with open(os.path.join(root, file), 'r') as file: 
                    try: 
                        obj  = hcl.load(file) 
                        data = json.dumps(obj) 
                        print(data) 
                    except ValueError as e:                                     # +4 (nesting = 2)
                        raise SystemExit(e) 
    return data                                                                 # total complexity = 19
"""

funcdef = ast.parse(script).body[0]

print(funcdef)

from cognitive_complexity.api import get_cognitive_complexity
print(get_cognitive_complexity(funcdef))

>18