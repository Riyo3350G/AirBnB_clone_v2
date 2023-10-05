#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers"""
from fabric.api import *
from os.path import exists
env.hosts = ['52.3.255.32', '18.208.120.88']


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if not exists(archive_path):
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
