"""Export environment variables from yaml file"""

import sys
import os
import yaml

path = sys.argv[1]
with open(path, 'r') as yaml_file:
    env = yaml.safe_load(yaml_file) or {}
print(' '.join(['{0}={1}'.format(var, val) for var,val in env.items()]))