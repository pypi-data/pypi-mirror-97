#!/usr/bin/env python
"""Extra instropection facilities.

This module provide extra utility functions, using the standard ``inspect``
module.
"""
from __future__ import print_function

import six

import inspect


def callerFrame(depth=1):
    """Get the frame of the calling function.

    Note that you should delete eferences to the returned value or risk
    garbage collection problems. For example dor this
    :<py>:

        fr = callerFrame()
        ...
        del fr

    :Return:
        The frame object of the calling function.

    """
    try:
        frInfo = inspect.stack()[depth + 1]
        frame, filename, lnum, funcname, context, xIdx = frInfo
        return frame
    finally:
        del frame


def callerLocation(depth=1):
    """Get the location of the calling function.

    :Return:
        A tuple of (filename, lnum)

    """
    try:
        frInfo = inspect.stack()[depth + 1]
        frame, filename, lnum, funcname, context, xIdx = frInfo
    finally:
        del frame
    return filename, lnum


def dumpStack(level=1):
    """Print a clean stack trace back.

    This tries to make the stack easier to follow by:

    - Hiding CleverSheep entries.
    - Hiding '<string>' entries.
    - Keeping file names relative to the 'suite' directory.

    The result is a lie, but normally more readily useful. It is only intended
    to be used for debugging.
    """
    import traceback
    from six.moves import cStringIO as StringIO

    cwd = os.path.dirname(os.path.dirname(__file__))
    stack = traceback.extract_stack()
    data = []
    maxLen = 0
    f = StringIO()
    for filename, lineNumber, functionName, text in stack[:-level]:
        if "/CleverSheep/" in filename:
            continue
        if filename == "<string>":
            continue
        location = "%s:%d %s" % (
            Files.relName(filename, cwd), lineNumber, functionName)
        data.append((location, text))
        maxLen = max(len(location), maxLen)

    f.write("Stack dump:\n")
    for location, text in data:
        f.write("    %-*s - %s\n" % (maxLen, location, text))
    print(f.getvalue())
