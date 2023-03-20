""" Модуль логгера. Записывает лог с ошибками в ./logs/err.log."""

import logging
import logging.config
import sys

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "{level: %(levelname)s | "
                      "logger: %(name)s | "
                      "time: %(asctime)s | "
                      "line №: %(lineno)s | "
                      "message: %(message)s}"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout
        },
        "file_info_utils": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "./logs/info.log",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
            "level": "DEBUG",
            "encoding": "utf8",
            "formatter": "base"
        },
        "file_errors_utils": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "./logs/err.log",
            "when": "H",
            "interval": 10,
            "backupCount": 1,
            "level": "ERROR",
            "encoding": "utf8",
            "formatter": "base"
        },
    },
    "loggers": {
        "logger_main": {
            "level": "DEBUG",
            "handlers": ["console", "file_info_utils"]
        },
        "logger_handler_high_low_price": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_get_meta_data": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_loader": {
            "level": "DEBUG",
            "handlers": ["console", "file_info_utils"]
        },
        "logger_handler_cmd_low": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_cmd_high": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_cmd_custom": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_filter_price": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_filter_meal_plan": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_filter_amenities": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        },
        "logger_handler_filter_star": {
            "level": "ERROR",
            "handlers": ["console", "file_errors_utils"]
        }
    }
}


logging.config.dictConfig(dict_config)

logger_root= logging.getLogger('')
logger_root.setLevel(logging.DEBUG)
