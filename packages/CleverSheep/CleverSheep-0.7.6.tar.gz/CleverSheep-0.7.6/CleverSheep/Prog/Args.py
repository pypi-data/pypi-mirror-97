#!/usr/bin/env python
"""Various functions that help handling of arguments.

It is often desirable to define functions that can, for example, accept either
a list or a simple value. This module provide support to help clean up such
code. For example, rather than
:<py>:

    def xxx(v):
        if v is None:
            v = []
        elif isinstance(v, six.string_types):
            v = [v]
        for el in v:
            ...

We have
:<py>:

    def xxx(v):
        v = listize(v)
        for el in v:
            ...
"""

import six


def iterise(arg):
    """Convert arg into an iterable.

    :Param arg:
        This may be a None, list, tuple, non-string iterable or single value.
        None is treated as a special case, yielding an empty iterator.
    :Return:
        An iterator for the supplied argument.
    """
    if arg is None:
        return iter([])
    if isinstance(arg, six.string_types):
        return iter([arg])
    if isinstance(arg, (list, tuple)):
        return iter(arg)
    try:
        it = iter(arg)
        return it
    except TypeError:
        pass
    return iter([arg])


def listise(arg):
    """Convert arg into a list.

    :Param arg:
        This may be a list, tuple, non-string iterable or single value.
    """
    return list(iterize(arg))


def tuplise(arg):
    """Convert arg into a tuple.

    :Param arg:
        This may be a list, tuple, non-string iterable or single value.
    """
    return tuple(iterize(arg))


iterize = iterise
listize = listise
tuplize = tuplise
