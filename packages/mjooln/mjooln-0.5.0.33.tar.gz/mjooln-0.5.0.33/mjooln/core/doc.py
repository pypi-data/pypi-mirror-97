import json
import simplejson
import yaml

from mjooln.core.dic import Dic, DicError
from mjooln.core.seed import Seed


class DocError(DicError):
    pass


class JSON:
    """Dict to/from JSON string, with optional human readable"""

    @classmethod
    def dumps(cls, dic, human=True, sort_keys=False, indent=4 * ' '):
        """Convert from dict to JSON string

        :param dic: Input dictionary
        :type dic: dict
        :param human: Human readable flag
        :param sort_keys: Sort key flag (human readable only)
        :param indent: Indent to use (human readable only)
        """
        if human:
            return simplejson.dumps(dic, sort_keys=sort_keys, indent=indent)
        else:
            return json.dumps(dic)

    @classmethod
    def loads(cls, json_string):
        """ Parse JSON string to dictionary

        :param json_string: JSON string
        :return: dict
        """
        return simplejson.loads(json_string)


class YAML:

    @classmethod
    def dumps(cls, dic):
        """
        Convert dictionary to yaml
        """
        return yaml.safe_dump(dic)

    @classmethod
    def loads(cls, yaml_str):
        """
        Convert yaml string to dictionary
        """
        return yaml.safe_load(yaml_str)


# TODO: Rewrite as serializer/deserializer
# TODO: In other words, doc will be dic with dates as strings.
# TODO: Atom can be builtin, otherwise it will be a bit tricky.
# TODO: SHould zulu/key/identity also be builtin?
class Doc(Dic):
    """
    Enables child classes to mirror attributes, dictionaries, JSON and
    YAML

    ..note:: to_doc and from_doc are meant to be overridden in child class if
    elements are not serializable
    """

    @classmethod
    def from_doc(cls, doc: dict):
        """
        Convert input dictionary to correct types and return object

        ..note:: Override in child class to handle custom types

        :param doc: Dictionary with serializable items only
        :return: New Doc object instantiated with input dictionary
        :rtype: Doc
        """
        return cls.from_dict(doc)

    @classmethod
    def from_json(cls,
                  json_string: str):
        doc = JSON.loads(json_string=json_string)
        return cls.from_doc(doc)

    @classmethod
    def from_yaml(cls,
                  yaml_string: str):
        doc = YAML.loads(yaml_string)
        return cls.from_doc(doc)

    def to_doc(self,
               ignore_private: bool = True):
        """
        Converts class attributes to dictionary of serialized attributes

        ..note:: Override in child class to handle custom types

        :param ignore_private: Ignore private flag
        :return: Dictionary of serialized objects
        """
        # doc = self.to_dict(ignore_private=ignore_private)
        doc = vars(self).copy()
        if ignore_private:
            pop_keys = [x for x in doc
                        if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                doc.pop(key)
        for key, item in doc.items():
            if isinstance(item, Doc):
                doc[key] = item.to_doc(ignore_private=ignore_private)
            elif isinstance(item, Seed):
                doc[key] = item.seed()

        return doc

    def to_json(self,
                human_readable: bool = False,
                ignore_private: bool = True):
        doc = self.to_doc(ignore_private=ignore_private)
        return JSON.dumps(doc, human=human_readable)

    def to_yaml(self,
                ignore_private: bool = True):
        doc = self.to_doc(ignore_private=ignore_private)
        return YAML.dumps(doc)

