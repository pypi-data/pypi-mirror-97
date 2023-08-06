import logging
import re
from contextlib import contextmanager
from functools import wraps
from typing import Tuple, Optional

from translucent.base import Status
from translucent.formatters import JSON


def to_kebab_case(s):
    with_underscore = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", with_underscore).lower()


@contextmanager
def extra(**fields):
    root = logging.getLogger()
    restore = {}
    for (i, handler) in enumerate(root.handlers):
        if isinstance(handler.formatter, JSON):
            restore[i] = handler.formatter
            handler.formatter = handler.formatter.clone_with_extra(fields)
    yield

    for (i, formatter) in restore.items():
        root.handlers[i].formatter = formatter


def _to_exception_metadata(exc: Exception) -> dict:
    extra = {"status": Status.FAILURE}
    if hasattr(exc, "code"):
        extra["type"] = exc.code
    else:
        extra["type"] = to_kebab_case(exc.__class__.__name__)
    return extra


def log_status(log, message: Optional[str] = None, non_fatal: Tuple[Exception, ...] = tuple()):
    def wrapper(func):
        msg = message if message is not None else func.__name__

        @wraps(func)
        def fn(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log.info(msg, extra={"status": Status.SUCCESS})
                return result
            except non_fatal as exc:
                log.warning(msg, extra=_to_exception_metadata(exc))
            except Exception as exc:
                log.warning(msg, extra=_to_exception_metadata(exc))
                raise exc

        return fn

    return wrapper
