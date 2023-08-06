class NetomException(Exception):
    """Base exception used by this module."""


class NetomValidationError(NetomException):
    """A validation error occurred."""
