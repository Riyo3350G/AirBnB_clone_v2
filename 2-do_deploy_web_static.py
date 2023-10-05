#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy"""
from fabric.api import *
from os.path import exists
env.hosts = ['52.3.255.32', '18.208.120.88']


def do_deploy(archive_path):
    """func that distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    try:
        # Extract relevant information from the archive path
        # Extract the filename from the path
        file_name = archive_path.split("/")[-1]
        # Extract filename without extension
        no_ext_file = file_name.split(".")[0]
        # Target directory path
        no_ext_path = "/data/web_static/releases/" + no_ext_file

        # Upload the archive to the /tmp/ directory on the remote server
        if put(archive_path, "/tmp/").failed is True:
            return False

        # Create the target directory on the remote server
        if run("mkdir -p /data/web_static/releases/{}/".
               format(no_ext_file)).failed is True:
            return False

        # Extract the archive contents into the target directory
        if run("sudo tar -xzf /tmp/{} -C {}".format(file_name, no_ext_path)).failed\
           is True:
            return False

        # Remove the uploaded archive from the /tmp/ directory
        if run("rm /tmp/{}".format(file_name)).failed is True:
            return False

        # Move the extracted files and directories to the target directory
        if run("sudo mv {}/web_static/* {}".format(no_ext_path, no_ext_path)).failed\
           is True:
            return False

        # Remove the redundant web_static subdirectory
        if run("rm -rf {}/web_static".format(no_ext_path)).failed is True:
            return False

        # Remove the existing symbolic link to /data/web_static/current
        if run("rm -rf /data/web_static/current").failed is True:
            return False

        # Create a new symbolic link to the deployed content as the new version
        if run("ln -s {} /data/web_static/current".format(no_ext_path)).failed\
           is True:
            return False
        
        print("New version deployed!")
        return True  # Deployment successful
    except Exception as e:
        return False  # Deployment failed
