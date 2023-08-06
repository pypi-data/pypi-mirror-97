class StarlingError(Exception):
    def __init__(self, message: str, extra: dict = None):
        self.message = message
        if extra is None:
            self.extra = dict()
        else:
            self.extra = extra

    def __str__(self):
        return f'{self.message} with {str(self.extra)}'


class AuthenticationError(StarlingError):
    """
    Error during authentication
    """
    pass


class RetryTaskExitError(StarlingError):
    """
    Error in retry logic
    Use if no further progress is required
    """
    pass


class RetryTaskSkipAuthError(StarlingError):
    """
    Error in retry logic
    Use if required except for authentication
    """
    pass


class RetryTaskError(StarlingError):
    """
    Error in retry logic
    Use if required from authentication
    """
    pass


class RetryTaskDoneError(StarlingError):
    """
    Error in retry logic
    Use if not required specific task to retry more
    """
    pass
