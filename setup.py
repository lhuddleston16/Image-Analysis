from setuptools import setup
import sys


def forbid_publish():
    argv = sys.argv
    blacklist = ["register", "upload"]

    for command in blacklist:
        if command in argv:
            values = {"command": command}
            print('Command "%(command)s" has been blacklisted, exiting...' % values)
            sys.exit(2)


forbid_publish()

setup(
    name="pachama_test",
    version="0.0.1",
    description="A package to extract values from raster files.",
    author="Levi Huddleston",
    packages=["pachama_test"],
    url="https://github.com/lhuddleston16/pachama_test",
)
