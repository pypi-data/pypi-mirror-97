import os
from logging.config import dictConfig

from . import dictutils

def get_simple_config(logfile=None, loglevel=None, logfmt=None, loggers=None, logging=None, **kwargs):
    """
        {
            "logfile": "LOG FILE PATH",
            "loglevel": "DEBUG/INFO/...",
            "logfmt": "default/json",
            "logging": {
                ...
            }
        }
    """
    config = logging or {}
    logfile = logfile or config.get("logfile", "app.log")
    loglevel = loglevel or config.get("loglevel", "INFO")
    logfmt = logfmt or config.get("logfmt", "default")
    loggers = loggers or {}

    # make sure log folder exists...
    logfolder = os.path.abspath(os.path.dirname(logfile))
    if not os.path.exists(logfolder):
        os.makedirs(logfolder, exist_ok=True)

    # fix windows log file rotating problem
    default_file_handler_settings = {
        "level": "DEBUG",
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": logfile,
        "when": "midnight",
        "interval": 1,
        "backupCount": 30,
        "formatter": "default",
    }
    json_file_handler_settings = {
        "level": "DEBUG",
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": logfile,
        "when": "midnight",
        "interval": 1,
        "backupCount": 30,
        "formatter": "json",
    }
    if os.name == "nt":
        default_file_handler_settings = {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": logfile,
            "formatter": "default",
        }
        json_file_handler_settings = {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": logfile,
            "formatter": "json",
        }
    
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "{asctime} {levelname} {pathname} {lineno} {module} {funcName} {process} {thread} {message}",
                "style": "{"
            },
            "message_only": {
                "format": "{message}",
                "style": "{",
            },
            "json": {
                "class": "jsonformatter.JsonFormatter",
                "format": {
                    "asctime": "asctime",
                    "levelname": "levelname",
                    "pathname": "pathname",
                    "lineno": "lineno",
                    "module": "module",
                    "funcName": "funcName",
                    "process": "process",
                    "thread": "thread",
                    "message": "message",
                },
            },
        },
        "handlers": {
            "default_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "default_file": default_file_handler_settings,
            "json_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
            "json_file": json_file_handler_settings,
        },
        "loggers": {
        },
        "root": {
            "handlers": [logfmt+"_file", logfmt+"_console"],
            "level": loglevel,
            "propagate": True,
        }
    }
    dictutils.deep_merge(logging_config, {"loggers": loggers})
    dictutils.deep_merge(logging_config, config)
    return logging_config

def setup(*args, **kwargs):
    config = get_simple_config(*args, **kwargs)
    dictConfig(config)
