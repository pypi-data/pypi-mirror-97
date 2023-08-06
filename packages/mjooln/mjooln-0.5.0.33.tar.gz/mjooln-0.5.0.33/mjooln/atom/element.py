import logging
import string

from mjooln.core.name import Name
from mjooln.core.seed import Seed
from mjooln.core.glass import Glass

logger = logging.getLogger(__name__)


class InvalidElement(Exception):
    pass


class Element(str, Seed, Glass):
    """
    Defines element string with limitations

    - Minimum length is 2
    - Allowed characters are

        - Lower case ascii ``a-z``
        - Digits ``0-9``
        - Underscore ``_``
    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - Can not contain double underscore since it acts as separator for elements
      in :class:`.Key`

    Sample elements::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'

    """
    REGEX = r'(?!.*__.*)[a-z0-9][a-z_0-9]*[a-z0-9]'

    #: Allowed characters
    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'

    #: Allowed first characters
    ALLOWED_STARTSWITH = string.ascii_lowercase + string.digits

    #: Allowed last characters
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    @classmethod
    def is_seed(cls, str_: str):
        if len(str_) == 1:
            if Name.MINIMUM_ELEMENT_LENGTH > 1:
                return False
            else:
                return str_ in cls.ALLOWED_STARTSWITH
        else:
            return super().is_seed(str_)

    def __new__(cls,
                element: str):
        # TODO: Add list as input, creating key with separator
        cls.verify_element(element)
        self = super().__new__(cls, element)
        return self

    def __repr__(self):
        return f'Element(\'{self}\')'

    def stub(self):
        return self.__str__()

    @classmethod
    def from_stub(cls, stub: str):
        return cls(stub)

    @classmethod
    def verify_element(cls, str_: str):
        """
        Verify that string is a valid element

        :param str_: String to verify
        :return: True if str_ is valid element, False if not
        """
        if not len(str_) >= Name.MINIMUM_ELEMENT_LENGTH:
            raise InvalidElement(
                f'Element too short. Element \'{str_}\' has '
                f'length {len(str_)}, while minimum length '
                f'is {Name.MINIMUM_ELEMENT_LENGTH}')
        if not str_[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidElement(f'Invalid startswith. Element \'{str_}\' '
                                 f'cannot start with \'{str_[0]}\'. '
                                 f'Allowed startswith characters are: '
                                 f'{cls.ALLOWED_STARTSWITH}')
        if not str_[-1] in cls.ALLOWED_ENDSWITH:
            raise InvalidElement(f'Invalid endswith. Element \'{str_}\' '
                                 f'cannot end with \'{str_[-1]}\'. '
                                 f'Allowed endswith characters are: '
                                 f'{cls.ALLOWED_ENDSWITH}')
        invalid_characters = [x for x in str_ if x not in
                              cls.ALLOWED_CHARACTERS]
        if len(invalid_characters) > 0:
            raise InvalidElement(
                f'Invalid character(s). Element \'{str_}\' cannot '
                f'contain any of {invalid_characters}. '
                f'Allowed characters are: '
                f'{cls.ALLOWED_CHARACTERS}')
        if Name.ELEMENT_SEPARATOR in str_:
            raise InvalidElement(
                f'Element contains element separator, which is '
                f'reserved for separating Elements in a Key.'
                f'Element \'{str_}\' cannot contain '
                f'\'{Name.CLASS_SEPARATOR}\'')


    # @classmethod
    # def elf(cls, element):
    #     """ Allows key class to pass through instead of throwing exception
    #
    #     :param element: Input element string or element class
    #     :type element: str or Element
    #     :return: Element
    #     """
    #     # TODO: Handle input and guess a conversion that would match criteria
    #     if isinstance(element, Element):
    #         return element
    #     else:
    #         return cls(element)
