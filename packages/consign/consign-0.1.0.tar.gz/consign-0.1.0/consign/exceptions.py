# -*- coding: utf-8 -*-

"""
consign.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Consign's exceptions.
"""


class InvalidDataType(TypeError):
    """The data provided was somehow invalid."""


class InvalidPath(ValueError):
    """The path provided was somehow invalid."""


# Warnings


class ConsignWarning(Warning):
    """Base warning for Consign."""
