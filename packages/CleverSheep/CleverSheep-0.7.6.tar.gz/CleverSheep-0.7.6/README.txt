===================================
A collection of re-usable packages.
===================================

Introduction
============

    This is the top-level package for various other general purpose packages.
    It exists in order keep the other packages tidily hidden within a single
    name space.

    It is not recommended CleverSheep be used for new projects.

    For more details see https://gitlab.com/LCaraccio/clever-sheep

Installation
============
    Run './setup.py build' and './setup.py install'

Dependencies
============

Mostly you only need Python, but...

1. The curses library is used and on some Linux distributions 'pycurses' is not
   installed by default.
2. If you are using tornado or twisted as your event loop manager they will need
   to be installed
3. six.
