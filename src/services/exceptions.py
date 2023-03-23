class ItemNotFoundException(Exception):
    """Raise when item not found in database"""

    pass


class DuplicatedItemException(Exception):
    """Raise when item already in database"""

    pass
