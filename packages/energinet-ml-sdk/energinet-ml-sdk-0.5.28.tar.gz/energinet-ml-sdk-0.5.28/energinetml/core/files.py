import os
import glob
import shutil
import tempfile
import contextlib


class FileMatcher(object):
    """
    TODO
    """
    def __init__(self, root_path, include, exclude=None, recursive=True):
        """
        :param str root_path:
        :param list[str] include:
        :param list[str] exclude:
        :param bool recursive:
        """
        self.root_path = root_path
        self.include = include
        self.exclude = exclude
        self.recursive = recursive

    def __iter__(self):
        """
        :rtype: typing.Iterable[str]
        """
        include_files = self.match_files(self.include)
        exclude_files = self.match_files(self.exclude) \
            if self.exclude is not None else set()

        return iter(include_files - exclude_files)

    def match_files(self, patterns):
        """
        :param list[str] patterns:
        :rtype: set[str]
        """
        all_matches = set()

        for pattern in patterns:
            matches = glob.iglob(
                pathname='%s/%s' % (self.root_path, pattern),
                recursive=self.recursive,
            )

            all_matches.update((
                os.path.relpath(path, self.root_path)
                for path in matches
                if os.path.isfile(path)
            ))

        return all_matches


@contextlib.contextmanager
def temporary_folder(files):
    """
    Returns a context manager which creates a temporary folder on the
    filesystem and copies files into the folder.

    The ´files` parameter is an iterable of tuples of (src, dst), where
    src is absolute path on the filesystem (a file to copy), and dst
    is the destination in the temporary folder relative to its root.

    Usage example:

        files_to_copy = [
            ('/home/folder/some-file.txt', 'some-file.txt'),
            ('/home/folder/another-file.txt', 'folder/some-file.txt'),
        ]

        with temporary_folder() as temp_path:
            # files are available in temp_path

    :param typing.Iterable[typing.Tuple[str, str]] files:
    :rtype: typing.ContextManager[str]
    """
    def __mkdir_and_copyfile(src, dst):
        if not os.path.isdir(os.path.split(dst)[0]):
            os.makedirs(os.path.split(dst)[0])
        shutil.copyfile(src, dst)

    with tempfile.TemporaryDirectory() as temp_folder_path:
        for src, dst in files:
            __mkdir_and_copyfile(src, os.path.join(temp_folder_path, dst))
        yield temp_folder_path
