"""Create cors.json file for bucket

The `origin` should be passed as the first function argument. If it is empty, 
the origin is assumed to be "".
"""

import json
import os
import sys

origin = sys.argv[1] if len(sys.argv) >= 2 else ""
cors_dir = os.path.dirname(os.path.abspath(__file__))
cors_path = os.path.join(cors_dir, 'cors.json')
with open(cors_path, 'r') as cors_file:
    cors = json.load(cors_file)
cors_rule = cors[0]
cors_rule['origin'] = [origin]
with open('cors.json', 'w') as new_cors_file:
    json.dump(cors, new_cors_file)