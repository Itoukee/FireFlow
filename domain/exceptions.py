class NotFoundError(Exception):
    """The resource does not exist"""


class ForbiddenError(Exception):
    """The context has not access"""
