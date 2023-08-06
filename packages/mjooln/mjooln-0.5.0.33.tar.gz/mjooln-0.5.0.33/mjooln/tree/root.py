from mjooln import Doc, File, Key, FileName, Folder, Atom, \
    Element, FileSystem, Identity


class RootError(Exception):
    pass


class NotRootException(RootError):
    pass


class ErraticWakeSleep(RootError):
    pass


# TODO: Cleanup name Root in exceptions to reflect actual class name
class Root:
    """
    Combination of a folder and a file that defines a particular spot in
    the file system.

    .. warning:: Root is primarily meant to be used for inheritance, and
        not direct use

    Root key follows limitations of class :class:`.Key`.
    If root key is ``julian``,
    the following triplet of rules define a folder as a valid Root:

    1. Folder path is ``../julian``
    2. Folder contains a JSON file with name ``.julian.json``
    3. JSON file contains a dictionary, where one top level key is ``_root``,
       containing a :class:`.Root.RootDic` with ``Atom.key = 'julian'``

    This triplet defines a Root as valid independent of file system, database
    entry or configuration file entry, allowing it to be used as a standalone
    knot of data, identifiable by shape and not identity.

    The Root class also stores all attributes, except private, in the JSON
    file. The key ``_root`` is reserved for class private attributes.
    """
    # TODO: Add atom and species description. Also needs to be planted
    # TODO: Change key to name?
    # TODO: Allow compression and encryption

    #: Root class identifier
    ROOT = Element('root')

    #: Current class species (this is Root)
    SPECIES = ROOT

    # # TODO: Fix hack
    # _FILE_WILDCARD = '.*.json'

    # TODO: Make docfile that will update file when a variable is changed or
    # TODO: added
    TRUNK = Doc

    @classmethod
    def is_root(cls, folder):
        """
        Checks if folder is a valid root

        :param folder: Folder to check
        :type folder: Folder
        :return: True if folder is root, False if not
        :rtype: bool
        """
        try:
            _ = cls(folder)
            return True
        except NotRootException:
            return False

    @classmethod
    def _append_if_root(cls, roots, folder):
        if cls.is_root(folder):
            roots.append(cls(folder))

    @classmethod
    def walk_roots(cls, folder):
        folder = Folder.glass(folder)
        for fo in FileSystem.walk(folder,
                                  include_folders=True,
                                  include_files=False):
            if cls.is_root(fo):
                yield cls(fo)

    @classmethod
    def list_roots(cls,
                   folder,
                   pattern: str = '*',
                   recursive: bool = False):
        folder = Folder.glass(folder)
        return [cls(x) for x in
                FileSystem.list_folders(folder,
                                        pattern=pattern,
                                        recursive=recursive)
                if cls.is_root(x)]

    @classmethod
    def plant(cls,
              folder,
              key,
              trunk: TRUNK = TRUNK()):
        """
        Create a new root in folder, with given key and kwargs

        :param folder: Folder where the root will be created
        :type folder: Folder
        :param key: Root key, following :class:`.Key` limitations
        :type key: Key
        :param kwargs: Attributes to add to root
        :return: Created root
        :rtype: Root
        """
        # TODO: Require Ground to plant Root?
        folder = Folder.glass(folder)
        key = Key.glass(key)
        if not folder.exists():
            raise RootError(f'Folder does not exist: {folder}; '
                            f'Cannot plant root in non existent folder. '
                            f'Use Folder.create() first')
        root_folder = folder.append(key)
        if root_folder.exists():
            raise RootError(f'Cannot plant root in when folder by same name '
                            f'exists: {root_folder}. '
                            f'Empty and remove folder first. '
                            f'Or use a different key.')
        root_folder.create()
        cls._make_file(root_folder, key, trunk)
        return cls(root_folder)

    @classmethod
    def _make_file(cls,
                   root_folder,
                   key,
                   trunk: TRUNK = TRUNK()):
        root_folder = Folder.glass(root_folder)
        key = Key.glass(key)
        file = cls._get_file(root_folder)
        if file.exists():
            raise RootError(f'Cannot make existing {cls._name()} file: '
                            f'{file}')
        doc = {
            'atom': Atom(key).to_doc(),
            'species': cls.SPECIES.stub(),
            'trunk': trunk.to_doc(),
        }
        file.write(doc)

    @classmethod
    def _get_file(cls,
                  folder: Folder):
        file_name = FileName.make(stub=Key(folder.name()),
                                  extension=FileName.YAML,
                                  is_hidden=True)
        return File.join(folder, file_name)

    # TODO: Make exception texts more elfish
    @classmethod
    def elf(cls, folder):
        """
        Converts an existing folder to root, tolerating missing file but not
        invalid key. If a folder already is a valid root, it will be returned
        as root. The folder name must be a valid :class:`.Key`

        :raise RootError: If file already exists, but does not have the right
            key, or if it has an invalid format
        :param folder: Folder to convert to root
        :type folder: Folder
        :param kwargs: Attributes to add to root file
        :return: New or existing root
        :rtype: Root
        """
        if isinstance(folder, cls):
            return folder
        if isinstance(folder, str):
            folder = Folder(folder)
        if isinstance(folder, Folder) and cls.is_root(folder):
            return cls(folder)

        if not isinstance(folder, Folder):
            raise NotRootException(f'Cannot make {cls._name()} of this '
                                   f'input: {folder.__repr__()}')
        key = folder.name()
        if not Key.is_seed(key):
            raise NotRootException(f'Cannot make {cls._name()} when folder '
                                   f'name is not a valid Key: {folder.name()}')
        key = Key(key)
        if not folder.parent().exists():
            raise NotRootException(f'Cannot make {cls._name()} without a '
                                   f'parent folder. Create one first, and '
                                   f'use {cls._name()}.plant()')
        if not folder.exists():
            folder = folder.parent()
            return cls.plant(folder, key)

        file = cls._get_file(folder)

        if not file.exists():
            cls._make_file(folder, key, trunk=cls.TRUNK())
            # return cls(folder)

        return cls(folder)

    @classmethod
    def _name(cls):
        return cls.__name__

    def __init__(self, folder):
        self.__elf = False
        self._folder = None
        self._key = None
        self._file = None
        self.atom = None
        self.species = None
        self.trunk = None
        if folder is None:
            raise NotRootException(f'NoneType object is not a valid'
                                   f'{self._name()}. '
                                   f'Use {self._name()}.plant()')
        self._folder = Folder.glass(folder)
        if not self._folder.exists():
            raise NotRootException(f'Folder does not exist: '
                                   f'{self._folder}; '
                                   f'Use {self._name()}.plant()')
        if not Key.is_seed(self._folder.name()):
            raise NotRootException(f'Folder name \'{self._folder.name()}\' '
                                   f'is not a valid key, i.e. folder is '
                                   f'not a valid {self._name()}')
        self._key = Key(self._folder.name())
        self._file = self._get_file(folder)
        if not self._file.exists():
            raise NotRootException(f'File does not exist: {self._file}; '
                                   f'This is not a valid {self._name()}')
        self.wake()
        self.validate()

    def __str__(self):
        return self._folder.__str__()

    def __repr__(self):
        return f'Root(\'{self}\')'

    def validate(self):
        """
        Verify that root is valid

        :raise NotRootException: If root is not valid
        """
        if self._folder.name() != self._key:
            raise NotRootException('Folder key mismatch')
        if self.atom.key() != self._key:
            raise NotRootException('Atom key folder key mismatch')
        if self.species != self.SPECIES:
            raise NotRootException('Species mismatch')

    def _read(self):
        doc = self._file.read()
        if doc is None or \
                'atom' not in doc or \
                'species' not in doc or \
                'trunk' not in doc:
            raise NotRootException(f'Invalid contents for {self._name()} in '
                                   f'file: {self._file}')
        atom = Atom.from_doc(doc['atom'])
        species = Key(doc['species'])
        trunk = self.TRUNK.from_doc(doc['trunk'])
        if species != self.SPECIES:
            raise NotRootException(f'Species mismatch. '
                                   f'Species asleep: {species};'
                                   f'Species awake: {self.SPECIES}')
        return atom, species, trunk

    def _write(self):
        doc = {
            'atom': self.atom.to_doc(),
            'species': self.species.seed(),
            'trunk': self.trunk.to_doc(),
        }
        self._file.write(doc)

    def asleep(self) -> bool:
        return self.atom is None and \
               self.species is None and \
               self.trunk is None

    def awake(self) -> bool:
        return not self.asleep()

    def wake(self):
        if self.awake():
            raise RootError(f'Already awake. Use touch()')
        self.atom, self.species, self.trunk = self._read()

    def touch(self):
        if self.asleep():
            self.wake()
            return
        atom, species, trunk = self._read()
        if atom != self.atom or species != self.species:
            raise ErraticWakeSleep(
                f'{self._name()} is neither asleep nor awake. '
                f'Asleep atom: {atom}; '
                f'Awake atom: {self.atom};'
                f'Asleep species: {species};'
                f'Awake species: {self.species}')
        if trunk != self.trunk:
            self._write()

    def sleep(self):
        self.touch()
        self.atom = None
        self.species = None
        self.trunk = None


    def walk(self,
             include_folders: bool = True,
             include_files: bool = True):
        for x in FileSystem.walk(self._folder,
                                 include_folders=include_folders,
                                 include_files=include_files):
            if x != self._file:
                yield x

    def files(self):
        return self.walk(include_files=True,
                         include_folders=False)

    def folders(self):
        return self.walk(include_files=False,
                         include_folders=True)

    def list(self,
             pattern: str = '*',
             recursive: bool = False):
        return [x for x in
                FileSystem.list(self._folder,
                                pattern=pattern,
                                recursive=recursive)
                if x != self._file]

    def list_files(self, pattern='*', recursive=False):
        paths = self.list(pattern=pattern, recursive=recursive)
        return [x for x in paths if isinstance(x, File)]

    def list_folders(self, pattern='*', recursive=False):
        paths = self.list(pattern=pattern, recursive=recursive)
        return [x for x in paths if isinstance(x, Folder)]

    # TODO: Add choice to remove root, but leave contents?
    def uproot(self,
               with_force: bool = False,
               key: Key = None,
               identity: Identity = None):
        """
        Remove root. If root has contents, use ``with_force=True`` and
        ``key=<root key>`` and ``identity=<root identity>`` to force this

        .. warning:: Forcing uproot will remove all contents recursively

        :param with_force: Flags forced uproot, which will remove all files
            and folders recursively
        :param key: Add key to verify forced uproot
        """
        # TODO: Handle hidden files..
        if len(self.list()) > 0:
            if with_force:
                if key == self.atom.key() and identity == self.atom.identity():
                    self.sleep()
                    self._folder.empty(name=key)
                else:
                    raise RootError(f'Root folder ({self}) is not empty. '
                                    f'Enter root key and identity with '
                                    f'uproot_with_force=True: '
                                    f'key={self.atom.key()}, '
                                    f'identity={self.atom.identity()}')
            else:
                raise RootError(f'Root folder ({self}) is not empty. '
                                f'Uproot with force to empty it: '
                                f'with_force=True')
        if self._file.exists():
            self.sleep()
            self._file.delete()
        self._folder.remove()
