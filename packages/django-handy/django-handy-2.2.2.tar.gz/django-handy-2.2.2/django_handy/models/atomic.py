from functools import wraps

from django.db import transaction


def call_on_commit(func):
    """
        Only call the decorated function at transaction commit.
        The return value will be ignored
    """

    @wraps(func)
    def handle(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return handle
