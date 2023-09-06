#!/usr/bin/python3
""" A module that generates archive the contents of web_static folder """
from fabric.api import local
from time import strftime


def do_pack():
    """ A fabric function to generate the archive content """

    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(timestamp))

        return "versions/web_static_{}.tgz".format(timestamp)

    except Exception as err:
        return None
