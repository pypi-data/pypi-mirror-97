"""Logging helper module standardizing logging and reducing boilerplate."""
import copy
import datetime
import functools
import logging
import logging.config
import pathlib
import sys
import typing as t

import crayons
import orjson
from pydantic import BaseSettings, Field

__all__ = ["setup_logging", "get_log_config"]


def setup_logging(**kwargs: t.Any) -> None:
    """Configure logging with settings from `get_log_config()`."""
    logging.config.dictConfig(get_log_config(**kwargs))


def get_log_config(**kwargs: t.Any) -> dict:
    """Get log config dict based on kwargs and/or envvars."""
    config = LogConfig(**kwargs)
    if config.handler == "file":
        color = False
    elif config.color is None:
        color = getattr(sys, config.handler).isatty()
    else:
        color = config.color
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "root": {
            "level": config.level,
            "handlers": [config.handler],
        },
        "loggers": {
            logger: {
                "level": level or config.level,
                "handlers": [config.handler],
            }
            for logger, level in config.loggers.items()
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": config.formatter,
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": config.formatter,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(config.filename),
                "delay": True,
                "maxBytes": config.max_bytes,
                "backupCount": config.backup_count,
                "formatter": config.formatter,
            },
        },
        "formatters": {
            "text": {
                "()": "fw_logging.Formatter",
                "fmt": config.fmt,
                "datefmt": config.datefmt,
                "color": color,
            },
            "json": {
                "()": "fw_logging.JSONFormatter",
                "tag": config.json_tag,
            },
        },
    }


class LogConfig(BaseSettings):  # pylint: disable=too-few-public-methods
    """Logging config."""

    class Config:  # pylint: disable=too-few-public-methods
        """Enable envvars with prefix `FW_LOG_`."""

        env_prefix = "fw_log_"

    level: str = Field("INFO", regex=r"TRACE|DEBUG|INFO|WARNING|ERROR|CRITICAL")
    handler: str = Field("stdout", regex=r"stdout|stderr|file")
    formatter: str = Field("text", regex=r"text|json")
    loggers: t.Dict[str, t.Optional[str]] = {}

    # options for the file handler
    filename: pathlib.Path = pathlib.Path("log.txt")
    max_bytes: int = 5 << 20
    backup_count: int = 10

    # options for the text formatter
    fmt: str = "{asctime}.{msecs:03.0f} {levelname} {caller} {message}"
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    color: t.Optional[bool]

    # options for the json formatter
    json_tag: t.Optional[str]


class Formatter(logging.Formatter):
    """Log formatter with color support.

    See https://github.com/encode/uvicorn/blob/0.12.3/uvicorn/logging.py
    """

    def __init__(
        self,
        fmt: t.Optional[str] = None,
        datefmt: t.Optional[str] = None,
        color: bool = False,
    ) -> None:
        """Initialize Formatter."""
        super().__init__(fmt=fmt, datefmt=datefmt, style="{")
        self.color = color

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Colorize levelname if color is enabled."""
        record_ = copy.copy(record)
        record_.__dict__["levelname"] = get_levelname(record.levelno, self.color)
        record_.__dict__["caller"] = get_caller(record, self.color)
        return super().formatMessage(record_)


COLORS = {
    "TRACE": "blue",
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "magenta",
}


@functools.lru_cache()
def get_levelname(levelno: int, color: bool = False) -> str:
    """Return 4 char long log level name, optionally colorized."""
    # pylint: disable=protected-access
    levelname = logging._levelToName.get(levelno, f"LV{levelno:02d}")[:4]
    if not color:
        return levelname
    cname = "white"
    for lname, cname in COLORS.items():
        if levelno <= getattr(logging, lname):
            break
    return str(getattr(crayons, cname)(levelname, always=True, bold=True))


def get_caller(record: logging.LogRecord, color: bool = False) -> str:
    """Return log record caller information, optionally colorized."""
    # pylint: disable=no-member
    caller = f"{record.name}:{record.module}:{record.lineno}"
    if not color:
        return caller
    return str(crayons.blue(caller, always=True))


class JSONFormatter(logging.Formatter):
    """JSON log formatter."""

    def __init__(self, tag: t.Optional[str] = None) -> None:
        """Initialize JSONFormatter."""
        self.tag = tag
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format the given LogRecord as a JSON string."""
        record_dict = {
            "msg": record.getMessage(),
            "lvl": record.levelname,
            "time": datetime.datetime.fromtimestamp(record.created),
            "caller": get_caller(record),
            "proc": record.process,
            "thrd": record.thread,
        }
        if record.exc_info:
            record_dict["exc"] = self.formatException(record.exc_info)
        if "tag" in record.__dict__ or self.tag:
            record_dict["tag"] = record.__dict__.get("tag") or self.tag
        # pylint: disable=c-extension-no-member
        return orjson.dumps(record_dict).decode()


def add_log_level(name: str, num: int) -> None:
    """Add a custom log level to the logging module.

    - add `name.upper()` attribute to the logging module with value num.
    - add `name.lower()` function/method to the logging module/logger class.
    """
    name = name.upper()
    func = name.lower()

    def _root_log(msg, *args, **kwargs):
        kwargs.setdefault("stacklevel", 3)
        logging.log(num, msg, *args, **kwargs)

    def _logger_log(self, msg, *args, **kwargs):
        if self.isEnabledFor(num):
            # pylint: disable=protected-access
            self._log(num, msg, args, **kwargs)

    _root_log.__doc__ = f"Log a message with severity '{name}' on the root logger."
    _logger_log.__doc__ = f"Log 'msg % args' with severity '{name}'."

    logging.addLevelName(num, name)
    setattr(logging, name, num)
    setattr(logging, func, _root_log)
    setattr(logging.getLoggerClass(), func, _logger_log)


add_log_level("TRACE", 5)
