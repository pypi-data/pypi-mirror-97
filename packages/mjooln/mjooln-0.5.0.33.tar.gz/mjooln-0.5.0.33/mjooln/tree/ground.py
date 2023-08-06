from functools import lru_cache

from mjooln import Name, Folder, Key, Element, Atom, FileName, File, \
    FileSystem
from mjooln.tree.root import Root
from mjooln.tree.tree import Tree


class GroundProblem(Exception):
    pass


class NoGround(Exception):
    pass


class Ground(Folder):
    """
    Custom hidden folder marking a specific folder as ``Ground``.

    Intended usage is for marking a location in a file system or network drive
    for simplified access. Roots in folder may be accessed directly, and
    attributes and statistics regarding all roots in the underlying folder
    structure may be stored in the ``cave``, which is a root folder hidden
    under ``ground``.
    """

    HOME = 'home'
    CAVE = Element('cave')
    GROUND_PREFIX = f'.ground{Name.CLASS_SEPARATOR}'
    CAVE_FOLDER_NAME = CAVE
    CAVE_FILE_NAME = FileName.make(CAVE,
                                   is_hidden=True,
                                   extension=FileName.YAML)

    # @classmethod
    # def _folder(cls, folder):
    #     if isinstance(folder, Folder):
    #         return folder
    #     return Folder(folder)

    @classmethod
    def _key_from_folder(cls, folder):
        return Key(folder.name().replace(cls.GROUND_PREFIX, ''))

    @classmethod
    def _get_ground_folder(cls, folder, key):
        return folder.append(cls.GROUND_PREFIX + key)

    @classmethod
    def _cave_and_file(cls, ground_folder, key):
        cave = Folder.join(ground_folder, cls.CAVE_FOLDER_NAME)
        cave_file = File.join(ground_folder, cls.CAVE_FILE_NAME)
        return cave, cave_file

    @classmethod
    def _get_key(cls, folder):
        ground_folders = FileSystem.list_folders(folder,
                                                 pattern=cls.GROUND_PREFIX +
                                                         '*')
        keys = [cls._key_from_folder(x) for x in ground_folders]
        if len(keys) > 1:
            raise GroundProblem(f'Found multiple grounds in folder: {folder}; '
                                f'Keys: {keys}')
        elif len(keys) == 0:
            raise NoGround(f'No ground found in folder: {folder}')
        return keys[0]

    @classmethod
    def is_in(cls, folder):
        """
        Check if folder is settled ground

        :raise GroundProblem: If folder contains multiple grounds, which is
            is a major problem
        :param folder: Folder to check
        :type folder: Folder
        :return: True if folder contains ground, False if not
        :rtype: bool
        """
        folder = Folder.glass(folder)
        num_paths = len(FileSystem.list_folders(folder,
                                                cls.GROUND_PREFIX + '*',
                                                recursive=False))
        if num_paths == 0:
            return False
        elif num_paths == 1:
            return True
        else:
            raise GroundProblem(f'Folder has multiple grounds: {folder}')

    @classmethod
    def _grounds(cls, folder, depth=0, max_depth=1):
        for fo in FileSystem.list_folders(folder):
            if cls.is_in(fo):
                yield Ground(fo)
            elif depth < max_depth:
                for ground in \
                        cls._grounds(fo, depth=depth + 1, max_depth=max_depth):
                    yield ground

    @classmethod
    def _locate(cls, folder, max_depth=1):
        folder = Folder.glass(folder)
        grounds = []
        if cls.is_in(folder):
            grounds.append(Ground(folder))
        for ground in cls._grounds(folder, depth=1, max_depth=max_depth):
            grounds.append(ground)
        return grounds

    @classmethod
    # TODO: Create test class
    def locate(cls, folders=None, max_depth=1):
        if not isinstance(folders, list):
            folders = [Folder.glass(folders)]
        grounds = []
        if not folders:
            folders = [Folder(x) for x in Folder.mountpoints()]
            home = Folder.home()
            if home not in folders:
                folders.append(home)
        for folder in folders:
            grounds += cls._locate(folder, max_depth=max_depth)
        return grounds

    @classmethod
    def settle(cls, folder, key):
        """
        Create new ground in the specified folder path, with the given key.

        :param folder: Folder to settle
        :type folder: Folder
        :param key: Ground key
        :type key: Key
        :return: Settled ground
        :rtype: Ground
        """
        folder = Folder.glass(folder)
        key = Key.glass(key)
        if not folder.exists():
            raise GroundProblem(f'Cannot settle ground in non existent '
                                f'path: {folder}')

        if cls.is_in(folder):
            raise GroundProblem(f'This folder has already been '
                                f'settled: {folder}; '
                                f'Key: {cls(folder).atom.key()}; '
                                f'Use Ground(folder), not settle()')

        ground_folder = cls._get_ground_folder(folder, key)
        ground_folder.create()
        atom = Atom(key)
        cave, cave_file = cls._cave_and_file(ground_folder, key)
        cave.create()
        cave_file.write(atom)
        return cls(folder)

    @classmethod
    @lru_cache()
    def home(cls):
        home = Folder.home()
        if not Ground.is_in(home):
            return cls.settle(home, key=cls.HOME)
        return cls(home)

    @classmethod
    @lru_cache()
    def crib(cls):
        home = cls.home()
        return home.cave()

    def __init__(self, folder):
        super().__init__()
        self.atom = None
        self.__cave = None
        key = self._get_key(folder)
        self._ground_folder = self._get_ground_folder(self, key)
        self.__cave, cave_file = self._cave_and_file(self._ground_folder, key)
        if not self.__cave.exists():
            raise GroundProblem(f'Missing cave folder: {self.__cave}')
        if not cave_file.exists():
            raise GroundProblem(f'Missing cave file: {cave_file}')
        self.atom = Atom.from_doc(cave_file.read())
        if self.atom.key() != key:
            raise GroundProblem(f'Ground key mismatch. '
                                f'Key in ground folder: {key}; '
                                f'Key in cave file: {self.atom.key()};'
                                f'Cave file: {cave_file}')

    def __repr__(self):
        return f'Ground(\'{self}\')'

    @lru_cache()
    def cave(self):
        return self.__cave

    def walk(self,
             include_files: bool = True,
             include_folders: bool = True):
        for x in FileSystem.walk(self,
                                 include_files=include_files,
                                 include_folders=include_folders):
            if not x.startswith(self._ground_folder):
                yield x

    def files(self):
        return self.walk(include_files=True,
                         include_folders=False)

    def folders(self):
        return self.walk(include_files=False,
                         include_folders=True)

    def list(self, pattern='*', recursive=False):
        paths = FileSystem.list(Folder(self),
                                pattern=pattern,
                                recursive=recursive)
        return [x for x in paths if not x.startswith(self._ground_folder)]

    def list_files(self, pattern='*', recursive=False):
        paths = self.list(pattern=pattern, recursive=recursive)
        return [x for x in paths if isinstance(x, File)]

    def list_folders(self, pattern='*', recursive=False):
        paths = self.list(pattern=pattern, recursive=recursive)
        return [x for x in paths if isinstance(x, Folder)]

    @classmethod
    def _roots(cls, folder, depth=0, max_depth=1):
        for fo in FileSystem.list_folders(folder):
            if Root.is_root(fo):
                yield Root(fo)
            elif depth < max_depth:
                for root in \
                        cls._roots(fo, depth=depth + 1, max_depth=max_depth):
                    yield root

    def roots(self, max_depth=1):
        # TODO: Rewrite to handle any species of root
        """
        Find all roots recursively from ground folder

        :return: List of all roots
        :rtype: [Root]
        """
        roots = []
        for r in self._roots(self, depth=1, max_depth=max_depth):
            roots.append(r)
        return roots

    @classmethod
    def _trees(cls, folder, depth=0, max_depth=1):
        for fo in FileSystem.list_folders(folder):
            if Tree.is_tree(fo):
                yield Tree(fo)
            elif depth < max_depth:
                for tree in \
                        cls._trees(fo, depth=depth + 1, max_depth=max_depth):
                    yield tree

    def trees(self, max_depth=1):
        # TODO: Somehow merge roots and trees
        """
        Find all roots recursively from ground folder

        :return: List of all roots
        :rtype: [Root]
        """
        trees = []
        for r in self._trees(self, depth=1, max_depth=max_depth):
            trees.append(r)
        return trees

    # def unsettle(self, force=False, key=None):
    #     if not self.__cave.is_empty():
    #         if not force or key != self.atom.key():
    #             raise GroundProblem(f'Cave is not empty. Use force=True, and '
    #                                 f'key={self.atom.key()}')
    #         self.__cave.empty()
    #     self.__cave.remove()
    #     _, cave_file = self._cave_and_file(self._ground_folder,
    #                                        self.atom.key())
    #     cave_file.delete()
    #     self.remove()
