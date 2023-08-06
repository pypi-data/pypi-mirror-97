#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import re

from collections import namedtuple
from pypermedia.client import SirenBuilder


# regex to convert from camelCase to snake_case
_reg = re.compile(r'(?!^)(?<!_)([A-Z])')


def siren_to_dict(o):
    return {
        attr: getattr(o, attr)
        for attr in dir(o)
        if attr[:1] != '_' and not callable(getattr(o, attr))
    }


def siren_to_entity(o):
    """
    Helper method that converts a siren entity into a namedtuple
    """
    def value_to_entity(v):
        return siren_to_entity(v) if isinstance(v, dict) else v

    # pypermedia does not do recursive translation
    # so we might get a mix of objects or dicts in here
    attrs = siren_to_dict(o) if not isinstance(o, dict) else o
    attrs = {
        to_snake_case(key): value_to_entity(value)
        for key, value in attrs.items()
    }
    return namedtuple(o.__class__.__name__, sorted(attrs))(**attrs)


def to_snake_case(s):
    # need to sanitise the string as in some cases the key might look like
    # 'Data Access'
    return _reg.sub(r'_\1', s.replace(' ', '_')).lower()


class PatchedSirenBuilder(SirenBuilder):

    def _construct_entity(self, entity_dict):
        """
        We need to patch the actions as there is no ``radio`` support
        on the current pypermedia version.

        To avoid code duplication, this function will attempt to call the parent
        and replace the created actions with our custom ones.
        """
        # pypermedia does not like any custom attributes
        # not even those in the spec
        for action in entity_dict.get("actions", []):
            if "allowed" in action:
                del action["allowed"]

        return super(PatchedSirenBuilder, self)._construct_entity(entity_dict)
