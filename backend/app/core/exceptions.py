class CompassError(Exception):
    """Base exception for domain-level API errors."""


class JourneyNotFoundError(CompassError):
    """Raised when a journey cannot be found."""


class InvalidProgressUpdateError(CompassError):
    """Raised when a progress update request is invalid."""
