#!/usr/bin/python3
"""Script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo,
using the function do_pack"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """create an archive of the web_static folder"""
    local("mkdir -p versions")
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_{}.tgz".format(current_date)
    res = local("tar -cvzf {} web_static".format(file_name))
    if res.succeeded:
        return file_name
    else:
        return None
