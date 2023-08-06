from __future__ import annotations
import datetime as dt
from enum import Enum
from pythonjsonlogger.jsonlogger import JsonFormatter, JsonEncoder


class JSON(JsonFormatter):
    _FIXED_FIELDS = ["namespace", "name"]
    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, *args, extra=None, **kwargs):
        self._fixed = {}
        for field in self._FIXED_FIELDS:
            if field not in kwargs:
                raise ValueError(f"Logging configuration requires field '{field}'")
            self._fixed[field] = kwargs.pop(field)

        self._args = args
        self._kwargs = kwargs
        self._kwargs["json_encoder"] = kwargs.get("json_encoder", CustomEncoder)
        super().__init__(*self._args, **self._kwargs)
        self._extra = extra or {}

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("time"):
            if record.created is not None:
                log_record["time"] = dt.datetime.fromtimestamp(record.created).strftime(
                    self._DATETIME_FORMAT
                )
            else:
                log_record["time"] = dt.datetime.utcnow().strftime(self._DATETIME_FORMAT)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        for (field, value) in self._fixed.items():
            log_record[field] = value
        for (field, value) in self._extra.items():
            log_record[field] = value

    def clone_with_extra(self, extra) -> JSON:
        return JSON(
            *self._args, extra={**self._extra, **extra}, **{**self._kwargs, **self._fixed}
        )


class CustomEncoder(JsonEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, Enum):
            return obj.value
        return JsonEncoder.default(self, obj)
