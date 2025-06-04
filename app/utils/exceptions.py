class AppException(Exception):
    """Base exception class for the application."""
    pass


class AuthenticationError(AppException):
    """Exception raised for authentication failures."""
    pass


class UserAlreadyExistsError(AppException):
    """Exception raised when trying to create a user that already exists."""
    pass


class UnauthorizedError(AppException):
    """Exception raised for unauthorized operations."""
    pass


class SecurityException(AppException):
    """Exception raised for security issues."""
    pass
