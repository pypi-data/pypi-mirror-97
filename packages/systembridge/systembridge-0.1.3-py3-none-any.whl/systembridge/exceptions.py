"""Bridge: Exceptions"""


class BridgeException(BaseException):
    """Raise this when something is off."""


class BridgeAuthenticationException(BridgeException):
    """Raise this when there is an authentication issue."""
