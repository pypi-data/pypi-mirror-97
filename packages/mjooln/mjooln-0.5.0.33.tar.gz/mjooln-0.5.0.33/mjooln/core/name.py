import re


class Name:
    """
    Module constants
    """
    #: Minimum length of Elements in Key
    MINIMUM_ELEMENT_LENGTH = 1

    #: Element separator in Key
    ELEMENT_SEPARATOR = '__'

    #: Class separator in Atom
    CLASS_SEPARATOR = '___'

    _CAMEL_TO_SNAKE = r'(?<!^)(?=[A-Z])'
    _SNAKE_TO_CAMEL = r'(.+?)_([a-z])'
    _RE_CAMEL_TO_SNAKE = re.compile(_CAMEL_TO_SNAKE)
    _RE_SNAKE_TO_CAMEL = re.compile(_SNAKE_TO_CAMEL)

    @classmethod
    def camel_to_snake(cls, camel: str):
        """
        Convert camel to snake::

            Name.camel_to_snake('ThisIsCamel')
                this_is_camel
        """
        return cls._RE_CAMEL_TO_SNAKE.sub('_', camel).lower()

    @classmethod
    def snake_to_camel(cls, snake: str):
        """
        Convert snake to camel::

            Name.snake_to_camel('this_is_snake')
                ThisIsSnake
        """
        # TODO: Implement regex instead
        return ''.join(x[0].upper() + x[1:] for x in
                       snake.split('_'))
