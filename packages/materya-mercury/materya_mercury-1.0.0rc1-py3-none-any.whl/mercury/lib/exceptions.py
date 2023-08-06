# Copyright (C) 2019 - 2021 Richard Kemp
# $Id: f3502c00f05b4dae5a1b07922954d9467929211c $
# -*- coding: utf-8; py-indent-offset:4 -*-

"""Mercury exceptions module."""


__copyright__ = "Copyright 2019 - 2021 Richard Kemp"
__revision__ = "$Id: f3502c00f05b4dae5a1b07922954d9467929211c $"
__all__ = [
    "ConnectionLostError",
    "NotValidPositionTypeError",
]


class ConnectionLostError(Exception):
    """Raised when a connector lost the connection to its endpoint.

    This exception is used as an all purposes to catch a disconnection for
    any reason and act on it, like trying to reconnect, before raising a real
    unavoidable exception.
    """


class NotValidPositionTypeError(Exception):
    """Raised when a position does not have a valid type property."""
    def __init__(self, msg, *args, **kwargs) -> None:
        """Override the default __init__.

        Provide a default message for the exception if none is passed.
        """
        if not msg:
            msg = "cmd must be 0 (BUY) or 1 (SELL)"
        super().__init__(msg, *args, **kwargs)
