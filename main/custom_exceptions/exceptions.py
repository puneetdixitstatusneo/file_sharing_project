class CustomValidationError(Exception):
    """
    This is the custom exception class for validation error. Raise this exception when request
    have invalid data.
    """

    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400


class UnauthorizedUserError(Exception):
    """
    This is the custom exception class to raise unauthorized user error
    """

    def __init__(self):
        super().__init__("Unauthorized user")
        self.status_code = 401


class EntityNotFoundError(Exception):
    """
    This is the custom exception class to raise an error if entity is not found.
    """

    def __init__(self, error_msg = None):
        super().__init__(error_msg or "Entity not found!!!")
        self.status_code = 404
