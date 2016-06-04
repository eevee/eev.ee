from __future__ import print_function

from datetime import datetime
from io import open
import os
import sys

from fabric.api import *
import fabric.contrib.project as project

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output-publish'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'rankurusu.veekun.com'
dest_path = '/var/www/eev.ee'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def new(title):
    from pelican.utils import slugify
    now = datetime.now()
    fn = "content/{date:%Y-%m-%d}-{slug}.markdown".format(
        date=now,
        slug=slugify(title),
    )

    with open(fn, 'w', encoding='utf8') as f:
        f.write(u"title: {}\n".format(title))
        f.write(u"date: {:%Y-%m-%d %H:%M}\n".format(now))
        f.write(u"category: blog\n")
        f.write(u"status: draft\n")
        f.write(u"\n")

    print("Created new post as {}".format(fn))
    sys.stdout.flush()

    # Switch to the editor
    EDITOR = os.environ['EDITOR']
    os.execlp(EDITOR, EDITOR, fn)

def build():
    local('pelican -s pelicanconf.py')

def rebuild():
    clean()
    build()

def regenerate():
    local('pelican -r -s pelicanconf.py')

def serve():
    local('cd {deploy_path} && python2 -m SimpleHTTPServer 8001'.format(**env))

def reserve():
    build()
    serve()

def preview():
    local('pelican -s publishconf.py')

def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))

@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
