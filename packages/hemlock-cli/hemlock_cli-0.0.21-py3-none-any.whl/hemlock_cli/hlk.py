"""Hemlock command line interface

Commands are categorized as:
0. Setup: install recommended software for Ubuntu on WSL
1. Initialization: initialize a new hemlock project and utilities
2. Content: modify the project content
3. Deploy: commands related to deployment
"""

import click

import os
from functools import wraps
from subprocess import call

__version__ = '0.0.21'

DIR = os.path.dirname(os.path.abspath(__file__))
SH_FILE = os.path.join(DIR, 'hlk.sh')

@click.group()
@click.version_option(__version__)
@click.pass_context
def hlk(ctx):
    pass

"""0. Setup"""
@click.command()
@click.argument('OS')
@click.option(
    '--chrome', is_flag=True,
    help='Set BROWSER environment variable pointing to chrome (WSL only)'
)
@click.option(
    '--chromedriver', is_flag=True,
    help='Install chromedriver'
)
@click.option(
    '--heroku-cli', is_flag=True,
    help='Install heroku command line interface'
)
def setup(os, chrome, chromedriver, heroku_cli):
    """Install recommended software"""
    if os not in ('win', 'wsl', 'mac', 'linux'):
        raise click.BadParameter('OS must be win, wsl, mac, or linux')
    args = (str(arg) for arg in (os, chrome, chromedriver, heroku_cli))
    if os == 'win':
        call(['sh', SH_FILE, 'setup', *args])
    else:
        call(['sudo', '-E', SH_FILE, 'setup', *args])

"""1. Initialization"""
@click.command()
@click.argument('project')
@click.argument('github-username')
@click.argument('github-token')
@click.option(
    '-r', '--repo', default='https://github.com/dsbowen/hemlock-template.git',
    help='Template project repository'
)
def init(project, github_username, github_token, repo):
    """Initialize Hemlock project"""
    call([
        'sh', SH_FILE, 'init', project, github_username, github_token, repo
    ])

@click.command('setup-venv')
@click.argument('OS')
@click.option('-n', '--name', default='', help='Kernel name')
def setup_venv(os, name):
    """Setup virtual environment (you should only need to use this on Windows git bash)"""
    if os not in ('win', 'wsl', 'mac', 'linux'):
        raise click.BadParameter('OS must be win, wsl, mac, or linux')
    call(['sh', SH_FILE, 'setup_venv', os, name])

@click.command('gcloud-bucket')
@click.argument('gcloud_billing_account')
def gcloud_bucket(gcloud_billing_account):
    """Create Google Cloud project and bucket"""
    call(['sh', SH_FILE, 'gcloud_bucket', gcloud_billing_account])

"""2. Content"""
@click.command()
@click.argument('packages', nargs=-1)
def install(packages):
    """Install Python package"""
    call(['sh', SH_FILE, 'install', *packages])

@click.command()
@click.option(
    '--keep-database', '-k', is_flag=True,
    help='Keep the database file'
)
def serve(keep_database):
    """Run Hemlock project locally"""
    call(['sh', SH_FILE, 'serve', str(keep_database)])

@click.command()
def rq():
    """Run Hemlock Redis Queue locally"""
    call(['sh', SH_FILE, 'rq'])

@click.command()
@click.option(
    '--staging', is_flag=True,
    help='Run the debugger in the staging environment'
)
@click.option(
    '--n-batches', '-n', default=1,
    help='Number of AI participant batches'
)
@click.option(
    '--batch-size', '-s', default=1,
    help='Size of AI participant batches'
)
def debug(staging, n_batches, batch_size):
    """Run debugger"""
    call([
        'sh', SH_FILE, 'debug', str(staging), str(n_batches), str(batch_size)
    ])

"""3. Deploy"""
@click.command()
def deploy():
    """Deploy application"""
    call(['sh', SH_FILE, 'deploy'])

@click.command()
def update():
    """Update application"""
    call(['sh', SH_FILE, 'update'])

@click.command()
def restart():
    """Restart application"""
    call(['sh', SH_FILE, 'restart'])

@click.command()
def production():
    """Convert to production environment"""
    call(['sh', SH_FILE, 'production'])

@click.command()
def destroy():
    """Destroy application"""
    call(['sh', SH_FILE, 'destroy'])

hlk.add_command(setup)
hlk.add_command(init)
hlk.add_command(setup_venv)
hlk.add_command(gcloud_bucket)
hlk.add_command(install)
hlk.add_command(serve)
hlk.add_command(rq)
hlk.add_command(debug)
hlk.add_command(deploy)
hlk.add_command(production)
hlk.add_command(update)
hlk.add_command(restart)
hlk.add_command(destroy)

if __name__ == '__main__':
    hlk()