class CabulBaseError(Exception):
    """Base error of cabul client."""


class NotFound(CabulBaseError):
    """Raised when API returns a 404."""


class APIError(CabulBaseError):
    """Raised when API returns an unexcepted status code."""

    def __init__(self, code: int = None):
        self.code = code


class ClientError(CabulBaseError):
    """Raised on Client error."""
