#!/usr/bin/python3
""" A module that generates and distributes an archive to your web server """
from fabric.api import put, run, local, env
from time import strftime
from os import path


env.hosts = ["54.173.130.243", "54.165.89.101"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_pack():
    """ A fabric function to generate the archive content """

    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as err:
        return None


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
        run("ln -s {} /data/web_static/current".format(fpath))
        return True
    except Exception as err:
        return False


def deploy():
    """ runs the 2 fabric functions """

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
