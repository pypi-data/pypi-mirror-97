# Copyright (C) 2019 - 2021 Richard Kemp
# $Id: 8ddd0823e4db6d71f4a7f46046142f95c02e46c7 $
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury Client module.

Provide

- Client superclass
"""

from __future__ import annotations


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id: 8ddd0823e4db6d71f4a7f46046142f95c02e46c7 $"
__all__ = [
    "Client",
]


from abc import ABCMeta, abstractmethod
from typing import TypeVar

from .baseclass import BaseClass


T = TypeVar("T")


class ClientMeta(ABCMeta, type(BaseClass)):
    """Client metaclass wrapper.

    This trick is needed when you want to use more than one metaclass
    for a given class.
    """
    pass


class Client(metaclass=ClientMeta):
    """Client abstract interface class.

    This is a superclass and it should not be call directly,
    superclass it instead.
    """
    @abstractmethod
    def connect(self) -> None:
        """Implement the client behavior to connect to the remote end."""

    @abstractmethod
    def request(self, payload: T, *, endpoint: str = None) -> T:
        """Implement a request with the given payload to the client."""
