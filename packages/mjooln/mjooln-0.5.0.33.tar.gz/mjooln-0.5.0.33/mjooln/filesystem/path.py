import os
import logging
import psutil
import socket
from sys import platform

from mjooln.core.glass import Glass
from mjooln.atom.zulu import Zulu

logger = logging.getLogger(__name__)


class PathError(Exception):
    pass


# TODO: Handle network drives (i.e. not mounted)?
# TODO: Add the lack of speed in documentation. Not meant to be used for
# TODO: for large folders (thats the whole point)
class Path(str, Glass):
    """ Absolute paths as a string with convenience functions

    No relative paths are allowed. Paths not starting with a valid
    mountpoint will be based in current folder.

    All backslashes are replaced with forward slash.
    """

    FOLDER_SEPARATOR = '/'
    PATH_CHARACTER_LIMIT = 256

    LINUX = 'linux'
    WINDOWS = 'windows'
    OSX = 'osx'
    PLATFORM = {
        'linux': LINUX,
        'linux2': LINUX,
        'darwin': OSX,
        'win32': WINDOWS,
    }

    @classmethod
    def platform(cls):
        """ Get platform name

        :raises PathError: If platform is unknown
        :return: Platform name (linux/windows/osx)
        :rtype: str
        """
        if platform in cls.PLATFORM:
            return cls.PLATFORM[platform]
        else:
            raise PathError(f'Unknown platform {platform}. '
                            f'Known platforms are: {cls.PLATFORM.keys()}')

    @classmethod
    def host(cls):
        """ Get host name

        Wrapper for ``socket.gethostname()``

        :return: Host name
        :rtype: str
        """
        return socket.gethostname()

    @classmethod
    def join(cls, *args):
        """ Join strings to path

        Wrapper for ``os.path.join()``

        Relative paths will include current folder::

            Path.current()
                '/Users/zaphod/dev'
            Path.join('code', 'donald')
                '/Users/zaphod/dev/code/donald'

        :return: Absolute path
        :rtype: Path
        """
        return cls(os.path.join(*args))

    @classmethod
    def mountpoints(cls):
        # TODO: Add limit on levels or something to only get relevant partitions
        """ List valid mountpoints/partitions or drives

        Finds mountpoints/partitions on linux/osx, and drives (C:, D:) on
        windows.

        :return: Valid mountpoints or drives
        :rtype: list
        """
        mps = [x.mountpoint.replace('\\', cls.FOLDER_SEPARATOR)
               for x in psutil.disk_partitions(all=True)
               if os.path.isdir(x.mountpoint)]
        # Remove duplicates (got double instance of root in a terraform vm)
        return list(set(mps))

    @classmethod
    def has_valid_mountpoint(cls, path_str):
        """ Flags if the path starts with a valid mountpoint

        :return: True if path has valid mountpoint, False if not
        :rtype: bool
        """
        return len([x for x in cls.mountpoints()
                    if path_str.startswith(x)]) > 0

    def __new__(cls, path: str):
        if not isinstance(path, str):
            raise PathError(f'Input to constructor must be of type str')
        if not os.path.isabs(path):
            path = path.replace('\\', cls.FOLDER_SEPARATOR)
            path = os.path.abspath(path)
        path = path.replace('\\', cls.FOLDER_SEPARATOR)
        if len(path) > cls.PATH_CHARACTER_LIMIT:
            logger.warning(f'Path exceeds {cls.PATH_CHARACTER_LIMIT} '
                           f'characters, which may cause problems on some '
                           f'platforms')
        # TODO: Add check on valid names/characters
        self = super().__new__(cls, path)
        if not cls.has_valid_mountpoint(path):
            raise PathError(f'Path does not have valid mountpoint '
                            f'for this platform: {path}')
        return self

    # Make pandas (and other libraries) recognize Path class as pathlike
    def __fspath__(self):
        return str(self)

    def __repr__(self):
        return f'Path(\'{self}\')'

    def name(self):
        """ Get name of folder or file

        Example::

            p = Path('/Users/zaphod')
            p
                '/Users/zaphod
            p.name()
                'zaphod'

            p2 = Path(p, 'dev', 'code', 'donald')
            p2
                '/Users/zaphod/dev/code/donald'
            p2.name()
                'donald'

        :return: Name of folder or file
        :rtype: str
        """
        return os.path.basename(self)

    def volume(self):
        """ Return path volume

        Volume is a collective term for mountpoint or drive

        :raises PathError: If volume cannot be determined
        :return: Volume of path
        :rtype: Path
        """
        # TODO: Consider removing this, since it does not handle network drives
        mountpoints = self.mountpoints()
        candidates = [x for x in mountpoints if self.startswith(x)]
        if len(candidates) > 1:
            candidates = [x for x in candidates
                          if not x == self.FOLDER_SEPARATOR]
        if len(candidates) == 1:
            return Path(candidates[0])
        else:
            # Find the longest matching candidate (should be the one)
            lens = [(len(x), x) for x in candidates]
            lens.sort(reverse=True)
            # Check that the two longest don't have same length
            # (this should not happen, since that would mean there were
            # two identical mountpoints)
            if lens[0][0] > lens[1][0]:
                return lens[0][1]
            else:
                raise PathError(
                    f'Could not determine volume for path: {self}; '
                    f'Based on candidates: {candidates};'
                    f'Avaliable mountpoints: {mountpoints}')

    def exists(self):
        """ Check if path exists

        Wrapper for ``os.path.exists()``

        :return: True if path exists, False otherwise
        :rtype: bool
        """
        return os.path.exists(self)

    def raise_if_not_exists(self):
        """ Raises an exception if path does not exist

        :raises PathError: If path does not exist
        """
        if not self.exists():
            raise PathError(f'Path does not exist: {self}')

    def is_volume(self):
        # TODO: Add handling of network drive
        # TODO: Check if found as network drive if not in mountpoints
        """ Check if path is a volume

        :raises PathError: If path does not exist
        :return: True if path is a volume, False if not
        :rtype: bool
        """
        if self.exists():
            return self in self.mountpoints()
        else:
            raise PathError(f'Cannot see if non existent path '
                            f'is a volume or not: {self}')

    def is_folder(self):
        """ Check if path is a folder

        :raises PathError: If path does not exist
        :return: True if path is a folder, False if not
        :rtype: bool
        """
        if self.exists():
            return os.path.isdir(self)
        else:
            raise PathError(f'Cannot determine if non existent path '
                            f'is a folder or not: {self}')

    def is_file(self):
        """ Check if path is a file

        :raises PathError: If path does not exist
        :return: True if path is a file, False if not
        :rtype: bool
        """
        if self.exists():
            return os.path.isfile(self)
        else:
            raise PathError(f'Cannot determine if non existent path '
                            f'is a file or not: {self}')

    def size(self):
        """ Return file or folder size

        .. warning:: If Path is a folder, ``size()`` will return a small number,
            representing the size of the folder object, not its contents.
            For finding actual disk usage of a folder, use
            :meth:`.Folder.disk_usage()`

        :raises PathError: If path does not exist
        :returns: File or folder size
        :rtype: int
        """
        if self.exists():
            return os.stat(self).st_size
        else:
            raise PathError(f'Cannot determine size of '
                            f'non existent path: {self}')

    def created(self):
        """ Get created timestamp

        :return: Timestamp created
        :rtype: Zulu
        """
        return Zulu.from_epoch(os.stat(self).st_ctime)

    def modified(self):
        """
        Get modified timestamp

        :returns: Timestamp modified
        :rtype: Zulu
        """
        return Zulu.from_epoch(os.stat(self).st_mtime)

    def parts(self):
        """ Get list of parts in path

        :returns: String parts of path
        :rtype: list
        """
        parts = str(self).split(self.FOLDER_SEPARATOR)
        # Remove empty first part (if path starts with /)
        if parts[0] == '':
            parts = parts[1:]
        return parts
