import os
import glob
import logging

from mjooln.filesystem.folder import Folder, FolderError
from mjooln.filesystem.file import File, FileError
from mjooln.filesystem.path import Path, PathError

logger = logging.getLogger(__name__)


class FileSystemError(Exception):
    pass


class FileSystem:
    # TODO: Move factoryish methods in here from other path classes
    # TODO: Add convenience methods for Tree
    # TODO: Make separate folder for filesystem. Core has crypt and dicdoc
    # TODO: Allow none as input to liste etc, so that a default can be used (current dir for ex)
    # TODO: Change all to staticmethod

    @classmethod
    def folder(cls, *args):
        return Folder.join(*args)

    @classmethod
    def file(cls, *args):
        return File.join(*args)

    # @classmethod
    # def _walk(cls,
    #          folder: Folder,
    #          folder_handler=None,
    #          file_handler=None):
    #     for root, fos, fis in os.walk(folder):
    #         if folder_handler:
    #             for fo in (cls.folder(root, x) for x in fos):
    #                 folder_handler(fo)
    #         if file_handler:
    #             for fi in (cls.file(root, x) for x in fis):
    #                 file_handler(fi)

    @classmethod
    def walk(cls,
             folder,
             include_files: bool = True,
             include_folders: bool = True):
        folder = Folder.glass(folder)
        for root, fos, fis in os.walk(folder):
            if include_folders:
                for fo in (cls.folder(root, x) for x in fos):
                    yield fo
            if include_files:
                for fi in (cls.file(root, x) for x in fis):
                    yield fi

    @classmethod
    def files(cls, folder):
        folder = Folder.glass(folder)
        return cls.walk(folder,
                        include_files=True,
                        include_folders=False)

    @classmethod
    def folders(cls, folder):
        folder = Folder.glass(folder)
        return cls.walk(folder,
                        include_files=False,
                        include_folders=True)

    @classmethod
    def list(cls,
             folder,
             pattern='*',
             recursive=False):
        folder = Folder.glass(folder)
        paths = folder.list(pattern=pattern, recursive=recursive)
        for i, path in enumerate(paths):
            try:
                if path.is_file():
                    paths[i] = File(path)
                elif path.is_folder():
                    paths[i] = Folder(path)
            except FileError or PathError or FolderError:
                # TODO: Handle links and other exceptions
                pass
        return paths

    @classmethod
    def list_files(cls,
                   folder,
                   pattern='*',
                   recursive=False):
        folder = Folder.glass(folder)
        paths = cls.list(folder,
                         pattern=pattern,
                         recursive=recursive)
        return [x for x in paths if isinstance(x, File)]

    @classmethod
    def list_folders(cls,
                     folder,
                     pattern='*',
                     recursive=False):
        folder = Folder.glass(folder)
        paths = cls.list(folder,
                         pattern=pattern,
                         recursive=recursive)
        return [x for x in paths if isinstance(x, Folder)]

    @classmethod
    def home(cls):
        return Folder.home()

    @classmethod
    def current(cls):
        return Folder.current()

    @classmethod
    def human_size(cls, size_bytes: int):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        size = size_bytes
        power_labels = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n] + 'B'

    @classmethod
    def bytes_to_human(cls,
                       size_bytes: int,
                       min_precision=5):
        value, unit = cls.human_size(size_bytes=size_bytes)
        len_int = len(str(int(value)))
        if len_int >= min_precision or unit == 'B':
            len_dec = 0
        else:
            len_dec = min_precision - len_int
        return f'{value:.{len_dec}f} {unit}'

    @classmethod
    def disk_usage(cls,
                   folder,
                   include_folders: bool = False,
                   include_files: bool = True):
        """
        Recursively determines disk usage of all contents in folder

        :param folder:
        :param include_folders:
        :param include_files:
        :raise FileSystemError: If folder does not exist
        :return: Disk usage of folder and subfolders
        :rtype: int
        """
        folder = Folder.glass(folder)
        if not folder.exists():
            raise FileSystemError(f'Cannot determine disk usage of '
                                  f'non existent folder: {folder}')
        size = 0
        for root, fos, fis in os.walk(folder):
            if include_folders:
                for fo in [cls.folder(root, x) for x in fos]:
                    size += fo.size()
            if include_files:
                for fi in [cls.file(root, x) for x in fis]:
                    size += fi.size()
        return size

    @classmethod
    def remove_empty_folders(cls, folder):
        folder = Folder.glass(folder)
        for root, folders, files in os.walk(folder):
            root = Folder(root)
            if root != folder and not folders and not files:
                root.remove()

    @classmethod
    def print(cls,
              folder,
              indent: int = 2,
              include_files: bool = True,
              include_folders: bool = True):
        # TODO: Redo with sequential walkthrough, and max_depth
        folder = Folder.glass(folder)
        for path in cls.walk(folder,
                             include_files=include_files,
                             include_folders=include_folders):
            level = path.replace(folder, '').count('/')
            path_indent = ' ' * indent * level
            path_tag = ''
            if path.is_folder():
                path_tag = '/'
            print(f'{path_indent}{path.name()}{path_tag}')
