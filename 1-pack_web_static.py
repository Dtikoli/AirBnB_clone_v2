#!/usr/bin/python3
""" A module that generates archive the contents of web_static folder """
from fabric.api import local
from time import strftime


def do_pack():
    """ A fabric function to generate the archive content """

    timestamp = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local(f"tar -czvf versions/web_static_{timestamp}.tgz web_static/")

        return f"versions/web_static_{timestamp}.tgz"

    except Exception as err:
        return None
