import logging
from contextlib import contextmanager
from translucent.formatters import JSON


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
