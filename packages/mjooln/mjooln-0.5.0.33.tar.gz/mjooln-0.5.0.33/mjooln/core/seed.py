import re


class BadSeed(Exception):
    pass


class Seed:
    """
    Convenience methods for string representation of an object

    Object can be created with the method ``from_seed()``, but the method
    must be overridden in child class. Find methods use the class variable
    ``REGEX``, which must also be overridden in child class

    If the seed has a fixed length, this can be specified in the class
    variable ``LENGTH``, and will speed up identification (or will it...)
    """

    #: Regex identifying seed must be overridden in child class
    REGEX = None

    #: If seed has a fixed length, override in child class
    LENGTH = None

    @classmethod
    def _search(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        return re.compile(cls.REGEX).search(str_)

    @classmethod
    def _exact_match(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        _regex_exact = rf'^{cls.REGEX}$'
        return re.compile(_regex_exact).match(str_)

    @classmethod
    def verify_seed(cls, str_: str):
        """
        Check if string is seed

        :raise BadSeed: If string is not seed
        :param str_: Seed to verify
        """
        if not cls.is_seed(str_):
            raise BadSeed(f'Sting is not seed: {str_}')

    @classmethod
    def is_seed(cls, str_: str):
        """
        Checks if input string is an exact match for seed

        :param str_: Input string
        :return: True if input string is seed, False if not
        """
        if cls.LENGTH and len(str_) != cls.LENGTH:
            return False
        return cls._exact_match(str_) is not None

    @classmethod
    def seed_in(cls, str_: str):
        """ Check if input string contains one or more seeds

        :param str_: String to check
        :type str_: str
        :return: True if input string contains one or more seeds, false if not
        """
        if cls._search(str_):
            return True
        else:
            return False

    @classmethod
    def find_seed(cls, str_: str):
        """
        Looks for and returns exactly one object from text

        Uses ``from_seed()`` to instantiate object from seed and will fail if
        there are none or multiple seeds.
        Use find_all() to return a list of identities in text, including
        an empty list if there are none

        :raise BadSeed: If none or multiple seeds are found in string
        :param str_: String to search for seed
        :type str_: str
        :return: Seed object
        """
        res = re.findall(cls.REGEX, str_)
        if len(res) == 1:
            return cls.from_seed(res[0])
        elif not res:
            raise BadSeed(
                f'No {cls.__name__} found in this text: \'{str_}\'; '
                f'Consider using find_seeds(), which will '
                f'return empty list if none are found.')
        else:
            raise BadSeed(
                f'Found {len(res)} instances of {cls.__name__} in this '
                f'text: \'{str_}\'; '
                f'Use find_all() to return a list of all instances'
            )

    @classmethod
    def find_seeds(cls,
                   str_: str):
        """ Finds and returns all seeds in text

        :type str_: str
        :return: List of objects
        """
        ids = re.findall(cls.REGEX, str_)
        return [cls.from_seed(x) for x in ids]

    @classmethod
    def from_seed(cls, str_: str):
        """
        Must be overridden in child class.

        Will create an object from seed

        :param str_: Seed
        :return: Instance of child class
        """
        raise BadSeed(f'Method from_seed() must be overridden '
                      f'in child class \'{cls.__name__}')

    def seed(self):
        """
        Get seed of current object.

        Default is ``str(self)``
        :return: Seed
        """
        return str(self)
