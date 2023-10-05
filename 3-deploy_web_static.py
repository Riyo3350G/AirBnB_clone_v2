#!/usr/bin/python3
"""Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an
archive to your web servers, using the function deploy"""
import os.path as path
from fabric.api import *
from datetime import datetime
env.hosts = ['52.3.255.32', '18.208.120.88']


def do_pack():
    """create an archive of the web_static folder"""
    try:
        if not path.exists("versions"):
            local("mkdir versions")
        current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(
            current_date))
        return ("versions/web_static_{}.tgz".format(current_date))
    except Exception:
        return None


def do_deploy(archive_path):
    """ fun: distributes an archive to your web servers """
    if not path.exists(archive_path):
        return False
    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Uncompress the archive to the folder
        file_name = archive_path.split("/")[-1]
        # file_name = file_name.split(".")[0]
        no_ext_path = file_name.split(".")[0]
        # no_ext_path = file_name
        path = "/data/web_static/releases/"
        # run("mkdir -p /data/web_static/releases/{}/".format(no_ext_path))
        run("mkdir -p {}{}/".format(path, no_ext_path))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name,
                                               path, no_ext_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext_path))
        run("rm -rf {}{}/web_static".format(path, no_ext_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path,
                                                          no_ext_path))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
