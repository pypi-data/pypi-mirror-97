import os
import json
import inspect
from dataclasses import dataclass, asdict


@dataclass
class Configurable(object):
    """
    TODO
    """

    class NotFound(Exception):
        pass

    # Constants
    CONFIG_FILE_NAME = None

    # Members
    path: str

    @classmethod
    def create(cls, path, **kwargs):
        """
        :param str path:
        :param typing.Dict kwargs:
        :rtype cls
        """
        obj = cls(path=path, **kwargs)
        obj.save()
        return obj

    @classmethod
    def from_config_file(cls, file_path):
        """
        :param str file_path:
        :rtype cls
        """
        with open(file_path) as f:
            return cls(path=os.path.split(file_path)[0], **json.load(f))

    @classmethod
    def from_directory(cls, path):
        """
        :param str path:
        :rtype: cls
        """
        if cls.CONFIG_FILE_NAME is None:
            raise RuntimeError('Attribute CONFIG_FILE_NAME is None')

        fp = locate_file_upwards(path, cls.CONFIG_FILE_NAME)

        if fp is not None:
            return cls.from_config_file(fp)
        else:
            raise cls.NotFound()

    def get_file_path(self, *relative_path):
        """
        Returns absolute path to a file at relative_path,
        where relative_path is relative to config file.

        :param str relative_path:
        :rtype: str
        """
        return os.path.abspath(os.path.join(self.path, *relative_path))

    def get_relative_file_path(self, absolute_path):
        """
        Provided an absolute file path, returns the path relative
        to config file.

        :param str absolute_path:
        :rtype: str
        """
        return os.path.relpath(absolute_path, self.path)

    def save(self):
        """
        Saved config as JSON to filesystem.
        """
        with open(self.get_file_path(self.CONFIG_FILE_NAME), 'w') as f:
            d = asdict(self)
            d.pop('path')
            json.dump(d, f, indent=4, sort_keys=True)


def locate_file_upwards(path, filename):
    """
    :param str path:
    :param str filename:
    :return: str
    """
    while 1:
        fp = os.path.join(path, filename)
        if os.path.isfile(fp):
            return fp
        elif path == '/':
            # TODO will not work on Windows
            return None
        else:
            path = os.path.abspath(os.path.join(path, '..'))
