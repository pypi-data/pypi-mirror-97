"""Permanently add new path to PATH

example:
$ python3 add_to_path.py /new/path
"""

import os
import sys

profile_path = os.path.join(os.environ.get('HOME'), '.bashrc')
profile = open(profile_path, 'a')
profile.write('\nexport PATH="{}:$PATH"'.format(sys.argv[1]))
profile.close()