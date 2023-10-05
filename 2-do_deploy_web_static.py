#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers,
using the function do_deploy"""
from fabric.api import *
from os.path import exists
env.hosts = ['52.3.255.32', '18.208.120.88']


def do_deploy(archive_path):
    """func that distributes an archive to your web servers"""
    try:
        if exists(archive_path) is False:
            return False
            # Extract relevant information from the archive path
            # Extract the filename from the path
            file_name = archive_path.split("/")[-1]
            # Extract filename without extension
            no_ext_file = file_name.split(".")[0]
            # Target directory path
            no_ext_path = "/data/web_static/releases/" + no_ext_file
            # Upload the archive to the /tmp/ directory on the remote server
            put(archive_path, "/tmp/")

            # Create the target directory on the remote server
            run("sudo mkdir -p {}".format(no_ext_path))

            # Extract the archive contents into the target directory
            run("sudo tar -xzf /tmp/{} -C {}".format(file_name, no_ext_path))

            # Remove the uploaded archive from the /tmp/ directory
            run("sudo rm /tmp/{}".format(file_name))

            # Move the extracted files and directories to the target directory
            run("sudo mv {}/web_static/* {}".format(no_ext_path, no_ext_path))

            # Remove the redundant web_static subdirectory
            run("sudo rm -rf {}/web_static".format(no_ext_path))

            # Remove the existing symbolic link to /data/web_static/current
            run("sudo rm -rf /data/web_static/current")

            # Create a new symbolic link to the deployed content
            run("sudo ln -s {} /data/web_static/current".format(no_ext_path))
            print("New version deployed!")
            return True  # Deployment was successful
    except Exception:
        return False  # Deployment failed
