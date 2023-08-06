import logging
import os
import shutil
import glob

from mjooln.filesystem.path import Path

logger = logging.getLogger(__name__)


class FolderError(Exception):
    pass


# TODO: Allow volume as folder
class Folder(Path):

    @classmethod
    def join(cls, *args):
        # Purely cosmetic for IDE
        return super().join(*args)

    @classmethod
    def home(cls):
        """ Get path to user home folder

        Wrapper for ``os.path.expanduser()``

        :return: Path to home folder
        :rtype: Path
        """
        return Folder(os.path.expanduser('~'))

    @classmethod
    def current(cls):
        """ Get current folder path

        Wrapper for ``os.getcwd()``

        :return: Path to current folder
        :rtype: Path
        """
        return cls(os.getcwd())

    def __new__(cls, path, *args, **kwargs):
        self = super().__new__(cls, path)
        # if cls.RESERVED in instance:
        #     raise FolderError(f'Folder path cannot contain \'{cls.RESERVED}\''
        #                       f'but was found here: {cls.RESERVED}')
        if self.exists():
            if self.is_file():
                raise FolderError(f'Path is a file, '
                                  f'not a folder: {self}')
        return self

    def __repr__(self):
        return f'Folder(\'{self}\')'

    def create(self, error_if_exists=True):
        """ Create new folder, including non existent parent folders

        :raises FolderError: If folder already exists,
            *and* ``error_if_exists=True``
        :param error_if_exists: Error flag. If True, method will raise an
            error if the folder already exists
        :type error_if_exists: bool
        :returns: True if it was created, False if not
        :rtype: bool
        """
        if not self.exists():
            os.makedirs(self)
            return True
        else:
            if error_if_exists:
                raise FolderError(f'Folder already exists: {self}')
            return False

    def touch(self):
        """ Create folder if it does not exist, ignore otherwise

        :return: True if folder was created, False if not
        :rtype: bool
        """
        self.create(error_if_exists=False)

    def untouch(self):
        """ Remove folder if it exists, ignore otherwise
        :return: True if folder was removed, False otherwise
        :rtype: bool
        """
        self.remove(error_if_not_exists=False)

    def parent(self):
        """ Get parent folder

        :return: Parent folder
        :rtype: Folder
        """
        return Folder(os.path.dirname(self))

    def append(self, *args):
        """ Append strings or list of strings to current folder

        Example::

            f = Folder.home()
            print(f)
                '/Users/zaphod'

            f.append('dev', 'code', 'donald')
                '/Users/zaphod/dev/code/donald'

            parts = ['dev', 'code', 'donald']
            f.append(parts)
                '/Users/zaphod/dev/code/donald'

        :param args: Strings or list of strings
        :return: Appended folder as separate object
        :rtype: Folder
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, list):
                return Folder.join(self, '/'.join(arg))
            else:
                return Folder.join(self, arg)
        else:
            return Folder.join(self, *args)

    def is_empty(self):
        """ Check if folder is empty

        :raise FolderError: If folder does not exist
        :return: True if empty, False if not
        :rtype: bool
        """
        if self.exists():
            return len(list(self.list())) == 0
        else:
            raise FolderError(f'Cannot check if non existent folder '
                              f'is empty: {self}')

    # TODO: Add test for empty, with missing name
    def empty(self, name: str):
        """  Recursively deletes all files and subfolders

        .. warning:: Be careful using this, as there is no double check
            before all contents is deleted. Recursively

        :param name: Name of folder. Required to verify deleting all
            contents
        :raise FolderError: If folder does not exist
        :return: Disk usage of folder and subfolders
        :rtype: int
        """
        if self.name() != name:
            raise FolderError(f'Name of folder required to verify '
                              f'deletion: name={self.name()}')
        if self.exists():
            for name in os.listdir(self):
                path = os.path.join(self, name)
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
        else:
            raise FolderError(f'Cannot empty a non existent folder: {self}')

    def remove(self,
               error_if_not_exists: bool = True):
        """ Remove folder

        Will raise an error if not empty

        :raises FolderError: If folder already exists, *and* ``error_if_exists``
            is set to ``True``
        :param error_if_exists: Error flag. If True, method will raise an
            error if the folder already exists
        :type error_if_exists: bool
        """
        if self.exists():
            os.rmdir(self)
        else:
            if error_if_not_exists:
                raise FolderError(f'Cannot remove a non existent '
                                  f'folder: {self}')

    def list(self,
             pattern: str = '*',
             recursive: bool = False):
        if not self.exists():
            raise FolderError(f'Cannot list non existent folder: {self}')

        if recursive:
            paths = glob.glob(self.append('**', pattern),
                              recursive=recursive)
        elif pattern is None:
            paths = os.listdir(self)
        else:
            paths = glob.glob(self.append(pattern))
        return [Path(x) for x in paths]
