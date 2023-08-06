"""Update environment file"""

import sys
import os
import yaml

path, key, val = sys.argv[1:]
with open(path, 'r') as yaml_file:
    env = yaml.safe_load(yaml_file)
env.update({key: val})
with open(path, 'w') as yaml_file:
    yaml.dump(env, yaml_file)