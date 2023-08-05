import contextlib
import logging
from functools import wraps
from typing import Callable, Iterable, Mapping

from django_redis import get_redis_connection
from redis.exceptions import LockError


logger = logging.getLogger(__name__)

NO_CACHE = object()
DEFAULT_LOCK_TIMEOUT = 10
KeyMakerType = Callable[[Iterable, Mapping], str]


def redis_client(write=True):
    return get_redis_connection(write=write)


@contextlib.contextmanager
def use_lock(key, timeout=DEFAULT_LOCK_TIMEOUT, blocking_timeout=None):
    """
    If blocking_timeout is specified, will proceed after
    blocking_timeout even without the lock obtained.
    Check the return value and abort if needed.
    """

    if timeout is None:  # Prevent locks without timeout set - it is too dangerous if the process dies
        timeout = DEFAULT_LOCK_TIMEOUT

    lock = redis_client().lock(f'use_lock:{key}', timeout=timeout, blocking_timeout=blocking_timeout)
    acquired = lock.acquire(blocking=True)
    try:
        yield acquired
    finally:
        if not acquired:
            return

        # Don't want failed lock release to break the whole application
        try:
            lock.release()
        except LockError as exc:
            logger.exception(str(exc))


def with_lock(
    key,
    timeout,
    blocking_timeout=None,
    proceed_without_lock=False,
):
    """
    If blocking_timeout is specified, and the lock is not obtained after blocking_timeout,
    behavior will depend on the proceed_without_lock.
    """

    def factory(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            with use_lock(key, timeout, blocking_timeout) as acquired:
                if not (acquired or proceed_without_lock):
                    return None
                return func(*args, **kwargs)

        return decorator

    return factory


def ensure_single(key, timeout):
    """Ensure function executes only single time simultaneously, other executions are aborted immediately"""
    return with_lock(key, timeout, blocking_timeout=0, proceed_without_lock=False)
