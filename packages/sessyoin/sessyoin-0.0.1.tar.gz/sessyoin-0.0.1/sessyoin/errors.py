class SessyoinBaseError(Exception):
    """Base error of sessyoin client."""


class NotFound(SessyoinBaseError):
    """Raised when API returns a 404."""


class APIError(SessyoinBaseError):
    """Raised when API returns an unexcepted status code."""

    def __init__(self, code: int = None):
        self.code = code


class ClientError(SessyoinBaseError):
    """Raised on Client error."""
