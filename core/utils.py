import time
from functools import wraps
from logging import Logger
from typing import Type


def retry(
    exceptions: tuple[Type[Exception], ...] = (Exception),  # type: ignore
    tries: int = 3,
    delay: float = 1,
    back_off: float = 1,
    logger: Logger | None = None,
):
    def decorator(func):

        @wraps(func)
        def retry_func(*args, **kwargs):
            _tries, _delay = tries, delay

            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    message = (
                        "Call to %s failed with exception %s. Retrying in %d second(s)."
                        % (func.__name__, str(e), _delay)
                    )

                    if logger:
                        logger.warn(message)
                    else:
                        print(message)

                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= back_off

            return func(*args, **kwargs)

        return retry_func

    return decorator
