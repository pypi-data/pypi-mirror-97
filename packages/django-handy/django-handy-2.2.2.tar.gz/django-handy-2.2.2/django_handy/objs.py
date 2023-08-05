from operator import attrgetter
from typing import Hashable, Iterable, List, Sized


class classproperty:
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)


def is_empty(val):
    """
        Check where value is logically `empty` - does not contain information.
        False and 0 are not considered empty, but empty collections are.
    """
    if val is None or isinstance(val, Sized) and len(val) == 0:  # Empty string is also Sized of len 0
        return True
    return False


def unique_ordered(sequence: Iterable[Hashable]) -> List:
    return list(dict.fromkeys(sequence))


def unique_objs(objs: List[object], unique_attrs: List[str]) -> List:
    """
       Get list of unique objs from sequence,
        preserving order when the objs first occurred in original sequence.
    """

    seen_obj_footprints = set()
    unique = []
    footprint_func = attrgetter(*unique_attrs)
    for obj in objs:
        obj_footprint = footprint_func(obj)
        if obj_footprint in seen_obj_footprints:
            continue

        seen_obj_footprints.add(obj_footprint)
        unique.append(obj)
    return unique
