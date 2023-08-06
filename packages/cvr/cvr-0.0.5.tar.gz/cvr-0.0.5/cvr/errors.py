class CVRError(Exception):
    """ All CVR-errors wrap CVRError """


class UnauthorizedError(CVRError):
    """ Raised when the API key is invalid """


class NotFoundError(CVRError):
    """ Raised when a requested entity was not found """
