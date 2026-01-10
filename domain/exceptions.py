class NotFoundError(Exception):
    """The resource does not exist"""


class Forbidden(Exception):
    """The context has not access"""
