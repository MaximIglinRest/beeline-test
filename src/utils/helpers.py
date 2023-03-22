import logging
from functools import wraps
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class MaxRetriesExceededException(Exception):
    pass


def backoff(
    start_sleep_time=0.1,
    factor=2,
    border_sleep_time=10,
    max_retries=5,
):
    """Механизм back-off для ожидания подключения к клиенту."""
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            t = start_sleep_time
            while iter := 0 < max_retries:  # noqa
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    actual_t = min(t, border_sleep_time)
                    logger.warning(
                        f"Failed to call {func.__name__}. "
                        f"Message: {e}. "
                        f"Retry in {actual_t} seconds."
                    )
                    sleep(actual_t)
                    t *= factor
                    iter += 1
            raise MaxRetriesExceededException

        return inner

    return func_wrapper
