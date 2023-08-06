"""
This module is internal module for mylogging library. Do not this if you are a user.
Use main __init__ module if you are user.

"""
from datetime import datetime
import warnings

from . import config


printed_infos = set()


def log_warn(message, log_type):
    """If _TO_FILE is configured, it will log message into file on path _TO_FILE. If not _TO_FILE is configured, it will
    warn or print INFO message.
    Args:
        message (str): Any string content of warning.
        log_type (ctr): Heading of warning if in file, generated automatically from __init__ module.
    """

    if config.TO_FILE:
        with open(config.TO_FILE, 'a+') as f:
            f.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{log_type}{message}")

    else:
        if log_type == 'INFO':
            if config.__DEBUG == 1:
                if message not in printed_infos:
                    print(message)
                    printed_infos.add(message)
            elif config.__DEBUG > 1:
                print(message)

        else:
            warnings.warn(message)


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors if raise.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """
    class X(str):
        def __repr__(self):
            return f"{message}"

    return X(message)


def colorize(message):
    """Add color to message - usally warnings and errors, to know what is internal error on first sight.
    Simple string edit.

    Args:
        message (str): Any string you want to color.

    Returns:
        str: Message in yellow color. Symbols added to string cannot be read in some terminals.
            If config COLOR is 0, it return original string.
    """

    if config.COLOR in [True, 1] or (config.COLOR == 'auto' and not config.TO_FILE):

        return f"\033[93m {message} \033[0m"

    else:
        return message
