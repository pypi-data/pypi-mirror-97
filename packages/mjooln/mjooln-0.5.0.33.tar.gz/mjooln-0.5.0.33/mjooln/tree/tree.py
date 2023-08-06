import logging

from mjooln import CryptError, Folder, File, Doc, Atom, AtomError, Element, \
    FileName
from mjooln.tree.root import Root, NotRootException
from mjooln.tree.leaf import Leaf, LeafError

logger = logging.getLogger(__name__)


class TreeError(Exception):
    pass


class NotTreeException(NotRootException):
    pass


class Tree(Root):
    """
    Folder structure based on strict :class:`.Atom` file names, and with an
    autonomous vocabulary.

    Create a new Tree by planting it in any folder, and with a key following
    the limitations of :class:`Key`::

        folder = Folder.home()
        key = 'oak'
        oak = Tree.plant(folder, key)

    Files outside the tree are defined as ``native``, while files in the
    tree are called ``Leaf``. Leaves are uniquely identified by
    :class:`.Atom`, which also defines their position in the folder
    structure underlying the tree.

    Leaves can be grown from a native file by defining a corresponding
    atom::

        native = File('some_outside_file.csv')
        atom = Atom(key='my_key')
        oak.grow(native, atom)

    The file may later be retrieved

    """

    #: Tree class identifier
    TREE = Element('tree')

    #: Current class identifier (this is a Tree)
    SPECIES = TREE

    class Trunk(Doc):

        def __init__(self,
                     extension='csv',
                     compress_all=False,
                     encrypt_all=False,
                     key_level=None,
                     date_level=0,
                     time_level=0):
            self.extension = extension
            self.compress_all = compress_all
            self.encrypt_all = encrypt_all
            self.key_level = key_level
            self.date_level = date_level
            self.time_level = time_level

    TRUNK = Trunk

    @classmethod
    def is_tree(cls, folder):
        """
        Check if folder is a tree

        :param folder: Folder to check
        :type folder: Folder
        :return: True if folder is a tree, False if not
        :rtype: bool
        """
        try:
            _ = cls(folder)
            return True
        except NotRootException:
            return False

    #
    # @classmethod
    # def plant(cls,
    #           folder: Folder,
    #           key: Key,
    #           trunk: Trunk = Trunk()):
    #     return super(Tree, cls).plant(folder=folder,
    #                                   key=key,
    #                                   trunk=trunk)

    #     # TODO: Add warning for long keys that may result in long path names
    #     # zulu: 23, id: 36, seps: 2 x 3, max_path:??
    #     """
    #     Creates a new tree
    #
    #     Folder specifies where the tree should be planted, while key will
    #     be the name of the tree folder
    #
    #     :param folder: Folder to plant the tree in
    #     :type folder: Folder
    #     :param key: Tree name or key
    #     :type key: Key
    #     :param extension: File extension for all files/leaves in tree
    #     :type extension: str
    #     :param compress_all: Flags compression of all files/leaves in tree
    #     :type compress_all: bool
    #     :param encrypt_all: Flags encryption of all files/leaves in tree
    #     :type encrypt_all: bool
    #     :param key_level: Key levels for folder structure
    #     :type key_level: int/None
    #     :param date_level: Date levels for folder structure
    #     :type date_level: int/None
    #     :param time_level: Time levels for folder structure
    #     :type time_level: int/None
    #     :param encryption_key: (*optional*) Encryption key used for
    #         encryption/decription of files/leaves in tree
    #     :type encryption_key: bytes
    #     :param kwargs: Additional attributes of tree
    #     :return: New tree
    #     :rtype: Tree
    #     """
    #     return = super(Tree, cls).plant(folder, key, trunk)
    #     if trunk._encryption_key:
    #         tree.add_encryption_key(encryption_key)
    #     return tree

    def __init__(self, folder, encryption_key=None):
        super().__init__(folder)
        self._encryption_key = None
        if self.species != self.SPECIES:
            raise NotTreeException(f'Species mismatch. '
                                   f'Expected: {self.SPECIES}, '
                                   f'Found: {self.species}')
        if encryption_key:
            self.add_encryption_key(encryption_key)

    def __repr__(self):
        return f'Tree(\'{self._folder}\')'

    def add_encryption_key(self, encryption_key=None):
        """
        Adds encryption key to trees with encryption activated. Encryption key
        may also be added in constructor. It will not be stored on disk, only
        in memory.

        :raise TreeError: If encryption is activated, but encryption_key is
            None
        :param encryption_key: Encryption key as defined by :class:`.Crypt`
        :type encryption_key: bytes
        """
        if self.trunk.encrypt_all and encryption_key is None:
            raise TreeError(f'Tree is encrypt_all, but no encryption_key '
                            f'supplied in constructor. Check Crypt class on '
                            f'how to make one, or disable encryption')
        self._encryption_key = encryption_key

    def _branch(self, atom):
        """
        Get the folder for the given atom

        :param atom: Input atom
        :type atom: Atom
        :return: Folder where a leaf with the input atom would be
        :rtype: Folder
        """
        levels = atom.levels(key_level=self.trunk.key_level,
                             date_level=self.trunk.date_level,
                             time_level=self.trunk.time_level)
        return self._folder.append(levels)

    def grow(self,
             native,
             atom=None,
             force_extension=False,
             delete_native=False,
             overwrite=False):
        """
        Add a file to the tree. A file outside of the tree is called ``native``
        while a file in the tree is called ``leaf``

        :param native: File to add to the tree
        :type native: File
        :param atom: Atom defining the contents of the file, if the file name
            is not a valid atom string
        :type atom: Atom
        :param force_extension: Flags forcing file extension to be the
            extension inherent in tree
        :type force_extension: bool
        :param delete_native: Flags whether to delete the native file after
            file has been copied to the tree structure
        :type delete_native: bool
        :param overwrite: Allow overwrite if leaf exists, i.e. a file with
            the same atom in tree
        :type overwrite: bool
        :return: New leaf in tree
        :rtype: Leaf
        """
        native = File.glass(native)
        if not native.exists():
            raise TreeError(f'Cannot grow Leaf from non existent '
                            f'path: {native}')
        if not native.is_file():
            raise TreeError(f'Native is not a file: {native}')
        if not force_extension and len(native.extensions()) != 1:
            raise TreeError(f'Leaves must have one extension, this native '
                            f'has none or multiple: {native.extensions()}. '
                            f'Use force_extension to set it to '
                            f'tree inherent: \'{self.trunk.extension}\'')

        if not atom:
            try:
                atom = Atom.from_seed(native.stub())
            except AtomError as se:
                raise TreeError(f'File name is not a valid '
                                f'atom: {native.name()}. '
                                f'Add atom as parameter to override '
                                f'file name.') from se

        if force_extension:
            extension = self.trunk.extension
        else:
            extension = native.extension()

        new_name = FileName.make(str(atom),
                                 extension,
                                 is_compressed=native.is_compressed(),
                                 is_encrypted=native.is_encrypted())

        if native.name() == new_name:
            new_name = None

        folder = self._branch(atom)
        if delete_native:
            file = native.move(folder, new_name, overwrite=overwrite)
        else:
            file = native.copy(folder, new_name, overwrite=overwrite)
        leaf = Leaf(file)
        logger.debug(f'Added leaf: {leaf}')
        leaf = self._shape(leaf)
        return leaf

    def leaf(self, atom):
        """
        Get the leaf defined by the given atom

        :param atom: Atom defining the leaf contents
        :type atom: Atom
        :return: Leaf defined by the atom
        :rtype: Leaf
        """
        atom = Atom.glass(atom)
        folder = self._branch(atom)
        file_name = FileName.make(str(atom),
                                  self.trunk.extension,
                                  is_compressed=self.trunk.compress_all,
                                  is_encrypted=self.trunk.encrypt_all)
        file = File.join(folder, file_name)
        return Leaf(file)

    def leaves(self, ignore_weeds: bool = True):
        # TODO: Rewrite to use FileSystem.walk()
        """
        Walk through all leaves in tree

        :return: Generator of leaves in tree
        :rtype: (Leaf)
        """

        for file in self.files():
            try:
                yield Leaf(file)
            except (LeafError, AtomError, ValueError) as e:
                if not ignore_weeds:
                    raise TreeError(f'File is not leaf: {e}; '
                                    f'Use prune() to remove weeds (not leaf), '
                                    f'or set ignore_weeds=True')

    def _shape(self, leaf):
        """
        Performs compress/decompress and/or encrypt/decrypt on a given file
        to match tree settings

        :param leaf: Leaf to shape
        :type leaf: Leaf
        :return: Shaped leaf
        :rtype: Leaf
        """
        try:
            if not leaf.is_compressed() and self.trunk.compress_all:
                if leaf.is_encrypted():
                    leaf = leaf.decrypt(self._encryption_key)
                leaf = leaf.compress()
            elif leaf.is_compressed() and not self.trunk.compress_all:
                if leaf.is_encrypted():
                    leaf = leaf.decrypt(self._encryption_key)
                leaf = leaf.decompress()
            if not leaf.is_encrypted() and self.trunk.encrypt_all:
                leaf = leaf.encrypt(self._encryption_key)
            elif leaf.is_encrypted() and not self.trunk.encrypt_all:
                leaf = leaf.decrypt(self._encryption_key)
        except CryptError as ce:
            raise TreeError(f'Invalid or missing encryption key while '
                            f'attempting reshape of {leaf}. '
                            f'Original error: {ce}')

        return Leaf.glass(leaf)

    def reshape(self, **kwargs):
        """
        Changes folder structure and/or compress/encrypt settings for all
        files in the tree from the input keyword arguments

        Performs compress/decompress and/or encrypt/decrypt on all files in
        tree to match tree settings for is_compressed and is_encrypted.

        Also prunes the tree moving files to correct folders, and deleting
        unused folders according to level settings

        .. note:: Folder and key cannot be changed

        :raise TreeError: If kwargs contain ``folder`` or ``key``
        :param kwargs: Attributes to change. Allowed attributes as in
            :meth:`plant()`
        """
        if not kwargs:
            logger.debug('No input arguments. Skipping reshape.')
        else:
            if 'folder' in kwargs:
                raise TreeError('Cannot change the folder of a tree '
                                'with reshape')
            if 'key' in kwargs:
                raise TreeError('Cannot change the key of a tree with '
                                'reshape')
            self.trunk.add(kwargs)
            self.touch()
            self.prune()

    def _prune_leaf(self, leaf):
        if not leaf.folder() == self._branch(leaf):
            leaf = leaf.move(self._branch(leaf))
            logger.debug(f'Move leaf: {leaf}')
        return leaf

    def prune(self, delete_not_leaf=False):
        """
        Moves files and deletes unused folders so that the tree structure
        matches level settings

        :param delete_not_leaf: Whether to delete files that are not leaf
        :type delete_not_leaf: bool
        """
        for file in self.files():
            try:
                leaf = Leaf(file)
                tmp = self._prune_leaf(leaf)
                _ = self._shape(tmp)
            except (AtomError, ValueError, LeafError):
                if delete_not_leaf:
                    logger.warning(f'Delete file that is not leaf: {file}')
                    file.delete()

        levels_and_folders = [(len(x.parts()), x) for x in self.folders()]
        levels_and_folders.sort(reverse=True)
        for _, folder in levels_and_folders:
            if folder.is_empty():
                folder.remove()

    def weeds(self):
        """
        Scans the tree for files with invalid shape, folder or name

        :return: Dictionary of weeds
        :rtype: dict
        """
        # TODO: Move weeds output to a custom class
        # TODO: Refactor to use walk, so that it can handle large trees, and
        # TODO: can be restarted
        leaves = list(self.leaves(ignore_weeds=True))
        files = list(self.files())
        not_leaves = len(files) - len(leaves)
        compression_mismatch = 0
        encryption_mismatch = 0
        for leaf in leaves:
            if leaf.is_compressed() != self.trunk.compress_all:
                compression_mismatch += 1
            if leaf.is_encrypted() != self.trunk.encrypt_all:
                encryption_mismatch += 1
        empty_folders = sum([x.is_empty() for x in self.folders()])
        return {
            'not_leaves': not_leaves,
            'compression_mismatch': compression_mismatch,
            'encryption_mismatch': encryption_mismatch,
            'empty_folders': empty_folders,
            'total_weeds': not_leaves +
                           compression_mismatch +
                           encryption_mismatch +
                           empty_folders
        }

    def total_weeds(self):
        """
        Scan tree and count total number of invalid leaves (weeds)

        :return: Total number of weeds in tree
        :rtype: int
        """
        weeds = self.weeds()
        return weeds['total_weeds']
