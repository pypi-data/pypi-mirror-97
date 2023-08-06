import logging

from mjooln.core.name import Name
from mjooln.core.seed import Seed
from mjooln.core.doc import Doc
from mjooln.core.glass import Glass

from mjooln.atom.zulu import Zulu
from mjooln.atom.key import Key
from mjooln.atom.identity import Identity

logger = logging.getLogger(__name__)


class AtomError(Exception):
    pass


class Atom(Doc, Seed, Glass):
    """
    Triplet identifier intended for objects and data sets alike

    Format: ``<zulu>___<key>___<identity>``

    :class:`.Zulu` represents t0 or creation time

    :class:`.Key` defines grouping of the contents

    :class:`.Identity` is a unique identifier for the contents

    Constructor initializes a valid atom, and will raise an ``AtomError``
    if a valid atom cannot be created based on input parameters.

    The constructor must as minimum have :class:`.Key` as input::

        a = Atom('some_key')
        a.key
            'some_key'
        a.zulu
            Zulu(2020, 5, 22, 13, 13, 18, 179169, tzinfo=<UTC>)
        a.identity
            '060AFBD5_D865_4974_8E37_FDD5C55E7CD8'
        str(a)
            '20200522T131318u179169Z___some_key___060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

    ``

    """

    REGEX = r'\d{8}T\d{6}u\d{6}Z\_\_\_[a-z][a-z_0-9]*[a-z0-9]\_\_\_' \
            r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{12}'

    @classmethod
    def from_seed(cls,
                  str_: str):
        if not cls.is_seed(str_):
            raise AtomError(f'Invalid atom seed: {str_}')
        zulu, key, identity = str_.split(Name.CLASS_SEPARATOR)
        return cls(key=Key(key),
                   zulu=Zulu.from_seed(zulu),
                   identity=Identity(identity))

    @classmethod
    def elf(cls, *args, **kwargs):
        if len(args) == 1 and kwargs is None:
            arg = args[0]
            if isinstance(arg, Atom):
                return arg
            if isinstance(arg, Key):
                return cls(arg)
            elif isinstance(arg, str):
                if Key.is_seed(arg):
                    return cls(arg)
                elif cls.is_seed(arg):
                    return cls.from_seed(arg)
                else:
                    raise AtomError(f'This input string is nowhere near '
                                    f'what I need to create an Atom: {arg}')
            elif Key.is_seed(arg):
                return cls(arg)
            else:
                raise AtomError(f'How the fuck am I supposed to create an atom '
                                f'based on this ridiculous excuse for an '
                                f'input: {arg} [{type(arg)}]')
        elif len(args) == 0:
            if 'key' not in kwargs:
                raise AtomError(f'At the very least, give me a key to work '
                                f'on. You know, key as thoroughly described '
                                f'in class Key')
            key = Key.elf(kwargs['key'])
            identity = None
            zulu = None
            if 'identity' in kwargs:
                identity = Identity.elf(kwargs['identity'])
            if 'zulu' in kwargs:
                zulu = Zulu.elf(kwargs['zulu'])
            return cls(key,
                       zulu=zulu,
                       identity=identity)
        raise AtomError(f'This is rubbish. Cannot make any sense of this '
                        f'mindless junk of input: '
                        f'args={args}; kwargs={kwargs}')

    @classmethod
    def default(cls):
        raise AtomError('Atom does not have a default value')

    @classmethod
    def from_dict(cls,
                  data: dict):
        zulu = data.pop('zulu')
        key = data.pop('key')
        identity = data.pop('identity')
        atom = cls(key=key, zulu=zulu, identity=identity)
        atom.add(data)
        return atom

    # TODO: Make key, identity, zulu private, with getters (keep hashable)
    def __init__(self,
                 key,
                 zulu: Zulu = None,
                 identity: Identity = None):
        """ Initializes a valid atom

        :param args: One argument is treated as a atom string and parsed.
        Three arguments is treated as (zulu, key, identity), in that order.
        :param kwargs: key, zulu, identity. key is required, while zulu and
        identity are created if not supplied.
        """
        super().__init__()
        # TODO: Replace with Key.glass()?
        if isinstance(key, str):
            if Key.is_seed(key):
                key = Key(key)
            elif Atom.is_seed(key):
                raise AtomError(f'Cannot instantiate with Atom seed. '
                                f'Use Atom.from_seed()')
            else:
                raise AtomError(f'Invalid key: {key} [{type(key).__name__}]')

        if not isinstance(key, Key):
            raise AtomError(f'Invalid instance of key: {type(key)}')

        if not zulu:
            zulu = Zulu()
        if not identity:
            identity = Identity()

        self.__zulu = zulu
        self.__key = key
        self.__identity = identity

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return Name.CLASS_SEPARATOR.join([str(self.__zulu),
                                          str(self.__key),
                                          str(self.__identity)])

    def __repr__(self):
        return f'Atom(key=\'{self.__key}\', ' \
               f'zulu={self.__zulu.__repr__()}, ' \
               f'identity={self.__identity.__repr__()})'

    def __hash__(self):
        return hash((self.__zulu, self.__key, self.__identity))

    def __lt__(self, other):
        return (self.__zulu, self.__key, self.__identity) < \
               (other.__zulu, other.__key, other.__identity)

    def __gt__(self, other):
        return (self.__zulu, self.__key, self.__identity) > \
               (other.__zulu, other.__key, other.__identity)

    def key(self):
        return self.__key

    def zulu(self):
        return self.__zulu

    def identity(self):
        return self.__identity

    def to_dict(self,
                ignore_private: bool = True,
                recursive: bool = False):
        return {
            'zulu': self.__zulu,
            'key': self.__key,
            'identity': self.__identity,
        }

    def to_doc(self,
               ignore_private: bool = True):
        # TODO: Replace stub with to_doc/from_doc (from Doc)
        return {
            'zulu': self.__zulu.iso(),
            'key': self.__key.seed(),
            'identity': self.__identity.seed(),
        }

    @classmethod
    def from_doc(cls, doc: dict):
        return cls(
            zulu=Zulu.from_iso(doc['zulu']),
            key=Key(doc['key']),
            identity=Identity(doc['identity']),
        )

    def with_separator(self,
                       separator: str):
        """ Atom string with custom separator

        :param separator: Custom separator
        :return: str
        """
        return separator.join(str(self).split(Name.CLASS_SEPARATOR))

    @classmethod
    def level_count(self,
                    level: int = None):
        if level is None or level < 0:
            return 1
        else:
            return level

    def levels(self,
               key_level: int = None,
               date_level: int = None,
               time_level: int = 0):
        """ Create list of levels representing the Atom

        Intended usage is for creating folder paths for atom files

        **None**: Full value

        **0**: No value

        **Negative**: Number of elements as string

        **Positive**: Number of elements as list

        Example::

            a = Atom(key='this__is__a_key')
            str(a)
                '20200522T181551u626184Z___this__is__a_key___F45A9C74_DC5D_48A6_9468_FC7E343EC554'
            a.levels()
                ['this__is__a_key', '20200522']
            a.levels(None, None, None)
                ['this__is__a_key', '20200522', '181551']
            a.levels(0, 0, 0)
                []
            a.levels(3, 2, 1)
                ['this', 'is', 'a_key', '2020', '05', '18']
            a.levels(-3, -2, -1)
                ['this__is__a_key', '202005', '18']

        :param key_level: Key levels
        :param date_level: Date levels
        :param time_level: Time levels
        :return: List of level strings
        :rtype: list
        """

        # TODO: Use this to make  level counter as well
        # TODO: Make this as classmethod
        def make(parts, level, sep=''):
            if level == 0:
                return []
            elif level > 0:
                return parts[:level]
            else:
                return [sep.join(parts[:-level])]

        if key_level is None:
            keys = [str(self.__key)]
        else:
            # TODO: Use key sep. At least as default
            keys = make(self.__key.elements(), key_level,
                        sep=Name.ELEMENT_SEPARATOR)

        zs = self.__zulu.str
        if date_level is None:
            dates = [zs.date]
        else:
            dates = make([zs.year, zs.month, zs.day], date_level)
        if time_level is None:
            times = [zs.time]
        else:
            times = make([zs.hour, zs.minute, zs.second], time_level)

        return keys + dates + times
