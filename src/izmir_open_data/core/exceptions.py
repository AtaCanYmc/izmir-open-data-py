class IzmirDataError(Exception):
    """Base exception for all Izmir Open Data errors."""
    pass

class APIError(IzmirDataError):
    """Raised when an API response indicates an error."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class ParsingError(IzmirDataError):
    """Raised when parsing response data fails."""
    pass
