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
        fpath = f"/data/web_static/releases/{fname}/"
        put(archive_path, '/tmp/')
        run(f"mkdir -p {fpath}")
        run(f"tar -zxvf /tmp/{arcfile} -C {fpath}")
        run(f"rm /tmp/{arcfile}")
        run(f"mv {fpath}/web_static/* {fpath}")
        run(f"rm -rf {fpath}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {fpath} /data/web_static/current")
        return True
    except Exception as err:
        return False
