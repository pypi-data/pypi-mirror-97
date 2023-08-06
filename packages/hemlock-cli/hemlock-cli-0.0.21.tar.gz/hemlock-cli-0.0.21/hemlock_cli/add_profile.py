"""Add a line to profile files

example:
$ python3 add_profile.py shell_type new_line
"""

import click

import os
import sys

# profile files used if none found in root directory
default_profile_file = {
    'bash': '.bashrc',
    'zsh': '.zshrc'
}

# resolution order for rofile files
profile_files = {
    'bash': [
        '.bash_profile',
        '.bash_login',
        '.profile',
        '.bashrc'
    ],
    'zsh': [
        '.zshenv',
        '.zprofile',
        '.zshrc',
        '.zlogin' 
    ]
}

def add_to_profile(shell_type, to_add):
    def get_profile_path():
        for f in profile_files[shell_type]:
            path = os.path.join(os.environ.get('HOME'), f)
            if os.path.exists(path):
                return path
        # no profile file found
        f = default_profile_file[shell_type]
        path = os.path.join(os.environ.get('HOME'), f)
        click.echo('\nWARNING: No profile file found. Creating a new profile file {}.'.format(path))
        return path

    path = get_profile_path()
    profile = []
    if os.path.exists(path):
        # read in the profile file
        with open(path, 'r') as profile_f:
            profile = profile_f.read()
        profile = profile.splitlines()
    # add new lines to the profile file, but avoid adding it multiple times
    profile = [line for line in profile if line != to_add] + [to_add]
    with open(path, 'w') as profile_f:
        profile_f.write('\n'.join(profile))

if __name__ == '__main__':
    # to_add is a line of code to add to the profile file
    shell_type, to_add = sys.argv[1:]
    assert shell_type in ('bash', 'zsh'), 'Invalid shell type. Shell type must be "bash" or "zsh"'
    add_to_profile(shell_type, to_add)