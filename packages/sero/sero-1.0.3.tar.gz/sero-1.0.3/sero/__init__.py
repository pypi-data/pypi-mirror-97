from os import path as _path

from sero.sero import Pipeline, parameterize

__all__ = ['Pipeline', 'parameterize']

with open(_path.join(_path.dirname(__file__), 'VERSION'), 'r') as version_file:
    VERSION = version_file.read()
