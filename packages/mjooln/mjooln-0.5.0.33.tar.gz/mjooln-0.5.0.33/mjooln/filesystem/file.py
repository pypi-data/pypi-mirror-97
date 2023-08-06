import gzip
import logging
import os
import shutil
import hashlib
from pathlib import Path as Path_

from mjooln.core.crypt import Crypt
from mjooln.core.doc import Doc, JSON, YAML
from mjooln.filesystem.path import Path
from mjooln.filesystem.folder import Folder

logger = logging.getLogger(__name__)


# TODO: Add yaml files


class FileError(Exception):
    pass


class FileName(str):
    JSON = 'json'
    YAML = 'yaml'
    TEXT = 'text'

    TYPES = [JSON, YAML, TEXT]

    MODE_TEXT = 't'
    MODE_BINARY = 'b'

    TYPE = {
        'json': {
            'extensions': ['json'],
            'mode': MODE_TEXT,
        },
        'yaml': {
            'extensions': ['yml', 'yaml'],
            'mode': MODE_TEXT,
        },
        'text': {
            'extensions': ['log', 'txt'],
            'mode': MODE_TEXT,
        }
    }

    #: Files with this extension will compress text before writing to file
    #: and decompress after reading
    COMPRESSED_EXTENSION = 'gz'

    #: Files with this extension will encrypt before writing to file, and
    #: decrypt after reading. The read/write methods therefore require a
    #: crypt_key
    ENCRYPTED_EXTENSION = 'aes'

    # #: Extensions reserved for compression and encryption
    # RESERVED_EXTENSIONS = [COMPRESSED_EXTENSION,
    #                        ENCRYPTED_EXTENSION]

    #: File names starting with this character will be tagged as hidden
    HIDDEN_STARTSWITH = '.'

    #: Extension separator. Period
    EXTENSION_SEPARATOR = '.'

    @classmethod
    def get_type(cls, extension):
        for key, item in cls.TYPE.items():
            if extension in item['extensions']:
                return key
        return None

    @classmethod
    def make(cls,
             stub: str,
             extension: str,
             is_hidden: bool = False,
             is_compressed: bool = False,
             is_encrypted: bool = False):
        """
        Create file name from stub and attributes

        :param stub: File stub, barring extensions and hidden startswith
        :param extension: File extension
        :param is_hidden: True tags file name as hidden
        :param is_compressed: True tags file name as compressed, adding the
            necessary extra extension
        :param is_encrypted:
        :return:
        """
        if stub.startswith(cls.HIDDEN_STARTSWITH):
            raise FileError(f'Stub cannot start with the hidden flag. '
                            f'Keep stub clean, and set is_hidden=True')
        if cls.EXTENSION_SEPARATOR in stub:
            raise FileError(f'Cannot add stub with extension '
                            f'separator in it: {stub}. '
                            f'Need a clean string for this')
        if cls.EXTENSION_SEPARATOR in extension:
            raise FileError(f'Cannot add extension with extension '
                            f'separator in it: {extension}. '
                            f'Need a clean string for this')
        names = [stub, extension]
        if is_compressed:
            names += [cls.COMPRESSED_EXTENSION]
        if is_encrypted:
            names += [cls.ENCRYPTED_EXTENSION]
        name = cls.EXTENSION_SEPARATOR.join(names)
        if is_hidden:
            name = cls.HIDDEN_STARTSWITH + name
        return cls(name)

    def __new__(cls, name):
        self = super().__new__(cls, name)
        self.hidden = name.startswith(self.HIDDEN_STARTSWITH)
        if self.hidden:
            name = name[1:]
        parts = name.split('.')
        while not parts[0]:
            parts = parts[1:]
        self.stub = parts[0]
        self.extensions = parts[1:]
        self.encrypted = self.extensions \
                         and self.extensions[-1] == cls.ENCRYPTED_EXTENSION
        if self.encrypted:
            self.extensions = self.extensions[:-1]
        self.compressed = self.extensions \
                          and self.extensions[-1] == cls.COMPRESSED_EXTENSION
        if self.compressed:
            self.extensions = self.extensions[:-1]
        self.extension = None
        if len(self.extensions) == 1:
            self.extension = self.extensions[0]
        self.type = None
        self.mode = ''
        if self.extension:
            self.type = cls.get_type(self.extension)
        if self.type:
            self.mode = cls.TYPE[self.type]['mode']
        return self

    def __repr__(self):
        return f'FileName(\'{self}\')'

    # def __init__(self, name: str):
    #     super(FileName, self).__init__(name)

    # def parts(self):


class File(Path):
    """
    Convenience class for file handling

    Create and read a file::

        f = File('my_file.txt')
        f.write('Hello world')
        f.read()
            'Hello world'
        f.size()
            11

    Compress and encrypt::

        fc = f.compress()
        fc.name()
            'my_file.txt.gz'
        fc.read()
            'Hello world'

        crypt_key = Crypt.generate_key()
        crypt_key
            b'aLQYOIxZOLllYThEKoXTH_eqTQGEnXm9CUl2glq3a2M='
        fe = fc.encrypt(crypt_key)
        fe.name()
            'my_file.txt.gz.aes'
        fe.read(crypt_key=crypt_key)
            'Hello world'

    Create an encrypted file, and write to it::

        ff = File('my_special_file.txt.aes')
        ff.write('Hello there', password='123')
        ff.read(password='123')
            'Hello there'

        f = open(ff)
        f.read()
            'gAAAAABe0BYqPPYfzha3AKNyQCorg4TT8DcJ4XxtYhMs7ksx22GiVC03WcrMTnvJLjTLNYCz_N6OCmSVwk29Q9hoQ-UkN0Sbbg=='
        f.close()

    .. note:: Using the ``password`` parameter, builds an encryption key by
        combining it with the builtin (i.e. hard coded) class salt.
        For proper security, generate your
        own salt with :meth:`.Crypt.salt()`. Then use
        :meth:`.Crypt.key_from_password()` to generate a crypt_key

    .. warning:: \'123\' is not a real password

    """
    _salt = b'O89ogfFYLGUts3BM1dat4vcQ'


    # TODO: Add binary flag based on extension (all other than text is binary..)
    # TODO: Facilitate child classes with custom read/write needs

    @classmethod
    def make(cls,
             folder,
             stub: str,
             extension: str,
             is_hidden: bool = False,
             is_compressed: bool = False,
             is_encrypted: bool = False):
        folder = Folder.glass(folder)
        file_name = FileName.make(stub=stub,
                                  extension=extension,
                                  is_hidden=is_hidden,
                                  is_compressed=is_compressed,
                                  is_encrypted=is_encrypted)
        return cls.join(folder, file_name)

    @classmethod
    def join(cls, *args):
        # Purely cosmetic for IDE
        return super().join(*args)

    @classmethod
    def home(cls,
             file_name: str):
        """
        Create a file path in home folder

        :param file_name: File name
        :type file_name: str
        :return: File
        :rtype: File
        """
        return cls.join(Folder.home(), file_name)

    @classmethod
    def _crypt_key(cls,
                   crypt_key: bytes = None,
                   password: str = None):
        """ Using a password will make a encryption_key combined with the
        internal class salt
        """
        if crypt_key and password:
            raise FileError('Use either crypt_key or password.')
        elif not crypt_key and not password:
            raise FileError('crypt_key or password missing')
        if crypt_key:
            return crypt_key
        else:
            return Crypt.key_from_password(cls._salt, password)

    def __new__(cls,
                path: str,
                is_binary: bool = False,
                *args, **kwargs):
        # TODO: Raise exception if reserved extensions are used inappropriately
        self = Path.__new__(cls, path)
        if self.exists():
            if self.is_volume():
                raise FileError(f'Path is volume, not file: {path}')
            elif self.is_folder():
                raise FileError(f'Path is existing folder, '
                                f'not file: {path}')

        self._name = FileName(self.name())
        return self

    def __repr__(self):
        return f'File(\'{self}\')'

    def parts(self):
        """
        Get file parts, i.e. those separated by period

        :return: list
        """
        return self._name.parts

    def touch(self):
        Path_(self).touch()

    def untouch(self, ignore_if_not_empty=False):
        """
        Delete file if it exists, and is empty

        :param ignore_if_not_empty: If True, no exception is raised if file
            is not empty and thus cannot be deleted with untouch
        :return:
        """
        if self.exists():
            if self.size() == 0:
                self.delete()
            else:
                if not ignore_if_not_empty:
                    raise FileError(f'Cannot untouch file '
                                    f'that is not empty: {self}; '
                                    f'Use delete() to delete a non-empty file')

    def extensions(self):
        """
        Get file extensions

        :return: List of file extensions
        :rtype: list
        """
        return self._name.extensions

    def is_hidden(self):
        """
        Check if file is hidden, i.e. starts with a period

        :return: True if hidden, False if not
        :rtype: bool
        """
        return self._name.hidden

    def is_encrypted(self):
        """
        Check if file is encrypted, i.e. ends with reserved extension \'aes\'

        :return: True if encrypted, False if not
        :rtype: bool
        """
        return self._name.encrypted

    def is_compressed(self):
        """
        Check if file is compressed, i.e. has reserved extension \'gz\'

        :return: True if compressed, False if not
        :rtype: bool
        """
        return self._name.compressed

    def stub(self):
        """
        Get file stub, i.e. the part of the file name bar extensions

        :return: File stub
        :rtype: str
        """
        return self._name.stub

    def extension(self):
        """
        Get file extension, i.e. the extension which is not reserved.
        A file is only supposed to have one extension that does not indicate
        either compression or encryption.

        :raise FileError: If file has more than one not reserved extensions
        :return: File extension
        :rtype: str
        """
        return self._name.extension

    def type(self):
        return self._name.type

    def get_mode(self):
        # Changed name from mode so as not to break pandas read.
        # TODO: Use common .mode variable to indicate mode
        # Apparently, that's the way to do it
        return self._name.mode

    def set_mode_binary(self):
        self._name.mode = self._name.MODE_BINARY

    def set_mode_text(self):
        self._name.mode = self._name.MODE_TEXT

    def md5_checksum(self):
        """
        Get MD5 Checksum for the file

        :raise FileError: If file does not exist
        :return: MD5 Checksum
        :rtype: str
        """
        if not self.exists():
            raise FileError(f'Cannot make checksum '
                            f'if file does not exist: {self}')
        md5 = hashlib.md5()
        with open(self, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def delete(self,
               missing_ok: bool = False):
        """
        Delete file

        :raise FileError: If file is missing, and ``missing_ok=False``
        :param missing_ok: Indicate if an exception should be raised if the
            file is missing. If True, an exception will not be raised
        :type missing_ok: bool
        :return: None
        """
        if self.exists():
            logger.debug(f'Delete file: {self}')
            os.unlink(self)
        elif not missing_ok:
            raise FileError(f'Tried to delete file '
                            f'that doesn\'t exist: {self}')

    def write(self, data, mode='w',
              crypt_key: bytes = None,
              password: str = None,
              # TODO: Handle JSON vs YAML write. I.e. maybe remove direct write
              human_readable: bool = True,
              **kwargs):
        """
        Write data to file

        For encryption, use either ``crypt_key`` or ``password``. None or both
        will raise an exception. Encryption requires the file name to end with
        extension \'aes\'

        :raise FileError: If using ``crypt_key`` or ``password``, and the
            file does not have encrypted extension
        :param data: Data to write
        :type data: str or bytes
        :param mode: Write mode
        :type mode: str
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        :param human_readable: JSON only, will write json to file with
            new lines and indentation
        :type human_readable: bool
        """
        # TODO: Require compression if file is encrypted?
        if self.is_encrypted():
            crypt_key = self._crypt_key(crypt_key, password)
        elif crypt_key or password:
            raise FileError(f'File does not have crypt extension '
                            f'({self._name.ENCRYPTED_EXTENSION}), '
                            f'but a crypt_key '
                            f'or password was sent as input to write.')
        if self.is_json():
            if isinstance(data, Doc):
                data = data.to_json(human_readable=human_readable)
            elif isinstance(data, dict):
                data = JSON.dumps(data)
        elif self.is_yaml():
            if isinstance(data, Doc):
                data = data.to_yaml()
            elif isinstance(data, dict):
                data = YAML.dumps(data)

        self.folder().touch()
        if self.is_compressed():
            self._write_compressed(data)
            if self.is_encrypted():
                if self.size() > 100000:
                    logger.warning('On the fly encrypt/compress not '
                                   'implemented. There is an extra read/write '
                                   'from/to disk. In other words, '
                                   'this is a hack.')
                # TODO: Refactor to write once, but verify zlib/gzip
                #  compatibility
                data = self._read(mode='rb')
                data = Crypt.encrypt(data, crypt_key)
                self.delete()
                self._write(data, mode='wb')
        else:
            if self.is_encrypted():
                if not isinstance(data, bytes):
                    data = data.encode()
                data = Crypt.encrypt(data, crypt_key)
                self._write(data, mode='wb')
            else:
                if mode and self.get_mode():
                    mode = mode + self.get_mode()
                self._write(data, mode=mode)

    def _write(self, data, mode='w'):
        with open(self, mode=mode) as f:
            f.write(data)

    def _write_compressed(self, content):
        if not isinstance(content, bytes):
            content = content.encode()
        with gzip.open(self, mode='wb') as f:
            f.write(content)

    def open(self, mode='r'):
        return open(self, mode=mode)

    def is_text(self):
        return self._name.type == self._name.TEXT

    def is_json(self):
        return self._name.type == self._name.JSON

    def is_yaml(self):
        return self._name.type == self._name.YAML

    def read(self, mode='r',
             crypt_key: bytes = None,
             password: str = None,
             num_lines: int = None,
             *args, **kwargs):
        """
        Read file

        If file is encrypted, use either ``crypt_key`` or ``password``.
        None or both will raise an exception. Encryption requires the file
        name to end with extension \'aes\'

        :raise FileError: If trying to decrypt a file without encryption
            extension
        :param mode: Read mode
        :param crypt_key: Encryption key
        :type crypt_key: bytes
        :param password: Password (will use class salt)
        :type password: str
        :param num_lines: Number of lines to read. ``None`` means read entire
            file (normal read), and this is also default
        :type num_lines: int
        :return: data
        :rtype: str or bytes
        """
        if not self.exists():
            raise FileError(f'Cannot read from file '
                            f'that does not exist: {self}')
        if self.is_encrypted():
            crypt_key = self._crypt_key(crypt_key, password)
        elif crypt_key or password:
            raise FileError(f'File does not have crypt extension '
                            f'({self._name.ENCRYPTED_EXTENSION}), '
                            f'but a crypt_key '
                            f'or password was sent as input to write.')
        if self.is_compressed():
            if self.is_encrypted():
                logger.warning('On the fly encrypt/compress not implemented. '
                               'There is an extra read/write from/to disk. '
                               'In other words, this is a hack.')
                # TODO: Refactor to read once, but
                #  verify zlib/gzip compatibility
                decrypted_file = self.decrypt(crypt_key, delete_original=False)
                data = decrypted_file._read_compressed(mode=mode)
                decrypted_file.delete()
            else:
                data = self._read_compressed(mode=mode, num_lines=num_lines)
        else:
            if self.is_encrypted():
                if num_lines is not None:
                    raise FileError(f'Read lines from encrypted file not '
                                    f'supported')
                data = self._read(mode='rb')
                data = Crypt.decrypt(data, crypt_key)
                if 'b' not in mode:
                    data = data.decode()
            else:
                mode = mode + self.get_mode()
                data = self._read(mode=mode,
                                  num_lines=num_lines)

        if self.is_json():
            if num_lines is not None:
                raise FileError(f'Cannot read lines from a json file: {self}')
            data = JSON.loads(data)
        elif self.is_yaml():
            if num_lines is not None:
                raise FileError(f'Cannot read lines from a yaml file: {self}')
            data = YAML.loads(data)

        return data

    def _read(self,
              mode='r',
              num_lines: int = None):
        with open(self, mode=mode) as f:
            if not num_lines:
                content = f.read()
            else:
                content = []
                for n in range(num_lines):
                    content.append(f.readline().strip())
                if len(content) == 1:
                    content = content[0]
        return content

    def _read_compressed(self,
                         mode='rb',
                         num_lines: int = None):
        with gzip.open(self, mode=mode) as f:
            if not num_lines:
                content = f.read()
            else:
                content = []
                for n in range(num_lines):
                    content.append(f.readline().strip())
                if len(content) == 1:
                    content = content[0]
        if 'b' not in mode:
            if not isinstance(content, str):
                if isinstance(content, list):
                    for n in range(len(content)):
                        if isinstance(content[n], bytes):
                            content[n] = content[n].decode()
                elif isinstance(content, bytes):
                    content = content.decode()

        return content

    def rename(self,
               new_name: str):
        """
        Rename file

        :param new_name: New file name, including extension
        :type new_name: str
        :return: A new File with the new file name
        :rtype: File
        """
        new_path = self.join(self.folder(), new_name)
        os.rename(self, new_path)
        return File(new_path)

    def folder(self):
        """
        Get the folder containing the file

        :return: Folder containing the file
        :rtype: Folder
        """
        return Folder(os.path.dirname(self))

    # def files(self,
    #           pattern: str = '*',
    #           recursive: bool = False):
    #     """
    #     Get a list of all files in folder containing the file
    #
    #     :param pattern: Wildcard or pattern
    #     :param recursive: Recursive flag. When True, all subfolders will be
    #         searched
    #     :return: List of files
    #     :rtype: list of File
    #     """
    #     files = self.folder().list(pattern='*', recursive=False)
    #     return [File(x) for x in files if x.is_file()]

    def move(self,
             new_folder: Folder,
             new_name: bool = None,
             overwrite: bool = False):
        """
        Move file to a new folder, and optionally a new name

        :param new_folder: New folder
        :type new_folder: Folder
        :param new_name: New file name (optional). If missing, the file will
            keep the same name
        :return: Moved file
        :rtype: File
        """
        new_folder.touch()
        if new_name:
            new_file = File.join(new_folder, new_name)
        else:
            new_file = File.join(new_folder, self.name())
        if not overwrite and new_file.exists():
            raise FileError(f'Target file already exists. '
                            f'Use overwrite=True to allow overwrite')
        if self.volume() == new_folder.volume():
            os.rename(self, new_file)
        else:
            shutil.move(self, new_file)
        return new_file

    def copy(self,
             new_folder: Folder,
             new_name: str = None,
             overwrite: bool = False):
        """
        Copy file to a new folder, and optionally give it a new name

        :param new_folder: New folder
        :type new_folder: Folder
        :param new_name: New file name (optional). If missing, the file will
            keep the same name
        :return: Copied file
        :rtype: File
        """
        if self.folder() == new_folder:
            raise FileError(f'Cannot copy a file '
                            f'to the same folder: {new_folder}')
        new_folder.touch()
        if new_name:
            new_file = File.join(new_folder, new_name)
        else:
            new_file = File.join(new_folder, self.name())
        if not overwrite and new_file.exists():
            raise FileError(f'Target file exists: {new_file}; '
                            f'Use overwrite=True to allow overwrite')
        shutil.copyfile(self, new_file)
        return new_file

    def compress(self,
                 delete_original: bool = True):
        """
        Compress file

        :param delete_original: If True, original file will be deleted after
            compression
        :return: New compressed file, with extension \'gz\'
        :rtype: File
        """
        if self.is_compressed():
            raise FileError(f'File already compressed: {self}')
        if self.is_encrypted():
            raise FileError(f'Cannot compress encrypted file: {self}. '
                            f'Decrypt file first')

        logger.debug(f'Compress file: {self}')
        old_size = self.size()
        new_file = File(f'{self}.gz')
        if new_file.exists():
            logger.warning(f'Overwrite existing gz-file: {new_file}')
        with open(self, 'rb') as f_in:
            with gzip.open(str(new_file), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_original:
            self.delete()
        new_file.compression_percent = 100 * (old_size - new_file.size()) \
                                       / old_size
        logger.debug(f'Compressed with compression '
                     f'{new_file.compression_percent:.2f}')
        return new_file

    def decompress(self,
                   delete_original: bool = True,
                   replace_if_exists: bool = True):
        """
        Decompress file

        :param delete_original: If True, the original compressed file will be
            deleted after decompression
        :param replace_if_exists: If True, the decompressed file will replace
            any already existing file with the same name
        :return: Decompressed file
        :rtype: File
        """
        if not self.is_compressed():
            raise FileError(f'File is not compressed: {self}')
        if self.is_encrypted():
            raise FileError(f'Cannot decompress encrypted file: {self}. '
                            f'Decrypt file first.')
        logger.debug(f'Decompress file: {self}')
        new_file = File(str(self).replace('.' + self._name.COMPRESSED_EXTENSION, ''))
        if new_file.exists():
            if replace_if_exists:
                logger.debug('Overwrite existing file: {}'.format(new_file))
            else:
                raise FileError(f'File already exists: \'{new_file}\'. '
                                f'Use replace_if_exists=True to ignore.')
        with gzip.open(self, 'rb') as f_in:
            with open(new_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        if delete_original:
            self.delete()
        new_file = File(new_file)
        new_file.compression_percent = None
        return new_file

    def encrypt(self,
                crypt_key: bytes,
                delete_original: bool = True):
        """
        Encrypt file

        :raise FileError: If file is already encrypted
        :param crypt_key: Encryption key
        :param delete_original: If True, the original unencrypted file will
            be deleted after encryption
        :return: Encrypted file
        :rtype: File
        """
        if self.is_encrypted():
            raise FileError(f'File is already encrypted: {self}')
        logger.debug(f'Encrypt file: {self}')
        encrypted_file = File(self + '.' + self._name.ENCRYPTED_EXTENSION)
        data = self._read(mode='rb')
        encrypted = Crypt.encrypt(data, crypt_key)
        encrypted_file._write(encrypted, mode='wb')
        if delete_original:
            self.delete()
        return encrypted_file

    def decrypt(self,
                crypt_key: bytes,
                delete_original: bool = True):
        """
        Decrypt file

        :raise FileError: If file is not encrypted
        :param crypt_key: Encryption key
        :param delete_original: If True, the original encrypted file will
            be deleted after decryption
        :return: Decrypted file
        :rtype: File
        """
        if not self.is_encrypted():
            raise FileError(f'File is not encrypted: {self}')

        logger.debug(f'Decrypt file: {self}')
        decrypted_file = File(self.replace('.' +
                                           self._name.ENCRYPTED_EXTENSION, ''))
        data = self._read(mode='rb')
        decrypted = Crypt.decrypt(data, crypt_key)
        decrypted_file._write(decrypted, mode='wb')
        if delete_original:
            self.delete()
        return decrypted_file
