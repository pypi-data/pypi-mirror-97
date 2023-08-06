import uuid

from mjooln.core.seed import Seed, re
from mjooln.core.glass import Glass


class IdentityError(Exception):
    pass


class Identity(str, Seed, Glass):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    REGEX = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
            r'\_[0-9A-F]{12}'

    REGEX_CLASSIC = r'[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}' \
                    r'\-[0-9a-f]{12}'
    REGEX_CLASSIC_COMPACT = r'[0-9a-f]{32}'
    LENGTH = 36

    @classmethod
    def from_seed(cls, str_: str):
        return cls(str_)

    @classmethod
    def is_classic(cls, str_: str):
        _regex_exact = rf'^{cls.REGEX_CLASSIC}$'
        return re.compile(_regex_exact).match(str_)

    @classmethod
    def is_classic_compact(cls, str_: str):
        _regex_exact = rf'^{cls.REGEX_CLASSIC_COMPACT}$'
        return re.compile(_regex_exact).match(str_)

    def __new__(cls,
                identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        elif cls.is_classic(identity):
            identity = identity.replace('-', '_').upper()
        elif len(identity) == 32 and cls.is_classic_compact(identity):
            identity = '_'.join([
                identity[:8],
                identity[8:12],
                identity[12:16],
                identity[16:20],
                identity[20:]
            ]).upper()
        elif not cls.is_seed(identity):
            raise IdentityError(f'String is not valid identity: {identity}')
        instance = super().__new__(cls, identity)
        return instance

    def __repr__(self):
        return f'Identity(\'{self}\')'

    @classmethod
    def elf(cls, str_):
        if isinstance(str_, Identity):
            return str_
        elif isinstance(str_, str):
            if cls.is_seed(str_) or \
                    cls.is_classic(str_) or \
                    (len(str_) == 32 and cls.is_classic_compact(str_)):
                return cls(str_)
            elif cls.is_classic(str_.lower()) or \
                    (len(str_) == 32 and cls.is_classic_compact(str_.lower())):
                return cls(str_.lower())

            # Try to find one or more identities in string
            ids = cls.find_seeds(str_)
            if len(ids) > 0:
                # If found, return the first
                return ids[0]
        raise IdentityError(
            f'This useless excuse for a string has no soul, '
            f'and hence no identity: \'{str_}\''
        )
