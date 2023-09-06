#!/usr/bin/python3
""" A module that distributes an archive to your web server """
from fabric.api import put, run, env
from os import path


env.hosts = ["54.173.130.243", "54.165.89.101"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
    """ A Fabric function to distribute the archive content"""

    if not path.exists(archive_path):
        return False
    try:
        arcfile = archive_path.split("/")[-1]
        fname = arcfile.split(".")[0]
        fpath = "/data/web_static/releases/{}/".format(fname)
        put(archive_path, '/tmp/')
        run("mkdir -p {}".format(fpath))
        run("tar -zxvf /tmp/{} -C {}".format(arcfile, fpath))
        run("rm /tmp/{}".format(arcfile))
        run("mv {}/web_static/* {}".format(fpath, fpath))
        run("rm -rf {}/web_static".format(fpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {fpath} /data/web_static/current".format(fpath))
        return True
    except Exception as err:
        return False
