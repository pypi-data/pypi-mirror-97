"""
mylogging
=========

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mylogging.svg)](https://pypi.python.org/pypi/mylogging/) [![PyPI version](https://badge.fury.io/py/mylogging.svg)](https://badge.fury.io/py/mylogging) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Malachov/mylogging.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Malachov/mylogging/context:python) [![Build Status](https://travis-ci.com/Malachov/mylogging.svg?branch=master)](https://travis-ci.com/Malachov/mylogging) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![codecov](https://codecov.io/gh/Malachov/mylogging/branch/master/graph/badge.svg)](https://codecov.io/gh/Malachov/mylogging)

My python warn-logging module. Based on debug value prints and logs warnings and errors. It's automatically colorized.
It log to console or it can log to file if configured.

Motivation for this project is to be able to have one very simple code base for logging and warning at once.
You can use one code for logging apps running on server (developer see if problems) and the same code for
info and warnings from running python code on computer in some developed library (user see when using code).

One code, two use cases.

Other reasons are to be able to recognise immediately if error is from my library or from some imported library.
Library try to be the simplest for use as possible (much simplier than logging or logguru).
Library have user friendly formatting.

Installation
------------

```console
pip install mylogging
```

How to
------

Example of set_warnings
-----------------------

First we can set warnings level with `set_warnings`

If log to console, override warnings display globally!!! => Use only in main script (not imported)
Mostly for developing apps.

If logging to file (good for web servers), warning levels are ignored!!! you don't have to call this function.

 - ignore warnings: debug=0,
 - display warnings once: debug=1,
 - display warnings always: debug=2,
 - stop warnings as errors: debug=3

```python
import mylogging

mylogging.set_warnings(debug=1)
```

You can ignore some warnings just by pass list of ignored warnings (any part of warning message suffice)
just add `ignored_warnings=["invalid value encountered in sqrt", "another ignored..."]` arg.

Example of warnings and logginng - info, warn, traceback
--------------------------------------------------------

```python
import mylogging

mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

# We can log / warn tracebacks from expected errors and continue runtime.

try:
    print(10 / 0)

except ZeroDivisionError:
    mylogging.traceback("Maybe try to use something different than 0.")

# Info will not trigger warning, but just print to console (but follows the rule in set_warnings(debug)).

mylogging.info("I am interesting info")
```


Logging to file
---------------

If you want to log to file, it's very simple just edit 'TO_FILE' to path with suffix (file will
be created if not exist).


```python

import mylogging

mylogging.config.TO_FILE = "path/to/my/file.log"  # You can use relative (just log.log)

# Then it's the same

import mylogging

mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

try:
    print(10 / 0)
except ZeroDivisionError:
    mylogging.traceback("Maybe try to use something different than 0.")

# You can use captions as well
mylogging.info("I am interesting info", caption="I am caption")

```

There is one more function you can use: `return_str`. It will return edited string (Color, indent and around signs).
Use case for that is raising your errors. You can see in one second, whether raise is your's or from imported library.

raise ModuleNotFoundError(mylogging.return_str("It's not in requirements because...", caption="Library not installed error"))


This is how the results look like.

<p align="center">
<img src="logging.png" width="620" alt="Plot of results"/>
</p>

For log file, just open example.log in your IDE.

CONFIG
------

AROUND
------

If log to file, whether separate logs with line breaks and ==== or shring to save space.

COLOR
-----

Colorize is automated. If to console, it is colorized, if to file, it's not (.log files
can be colorized by IDE).

If you have special use case (for example pytest logs on CI/CD), you can override value from auto

```python
mylogging.config.COLOR = 0  # Turn off colorization on all functions to get rid of weird symbols
```
"""

import warnings
import traceback as trcbck
import os
import pygments
from pygments.lexers.python import PythonTracebackLexer
from pygments.formatters import TerminalFormatter
import textwrap

from . import config
from .misc import log_warn, colorize, objectize_str


__version__ = "2.0.4"
__author__ = "Daniel Malachov"
__license__ = "MIT"
__email__ = "malachovd@seznam.cz"


# To enable colors in cmd...
os.system('')


def set_warnings(debug=1, ignored_warnings=[], ignored_warnings_module_category=[]):
    """Define debug type. Can print warnings, ignore them or stop as error.

    Note:
        !!! Globally overwritewarnings coping - even outside calling script.

    Args:
        debug (int): If 0, than warnings are ignored, if 1, than warning will be displayed just once, if 2,
            program raise error on warning and stop.
        ignored_warnings (list): List of warnings (any part of inner string) that will be ignored even if debug is set.
            Example ["AR coefficients are not stationary.", "Mean of empty slice",]
        ignored_warnings_module_category (list): List of tuples (string of module that raise it and warning type) that will be ignored even if debug is set.
            Example [('statsmodels.tsa.arima_model', FutureWarning)]
    """

    if debug == 0:
        config.__DEBUG = 0
        warnings.filterwarnings('ignore')

    elif debug == 1:
        config.__DEBUG = 1
        warnings.filterwarnings('once')

    elif debug == 2:
        config.__DEBUG = 2
        warnings.filterwarnings('always')

    elif debug == 3:
        config.__DEBUG = 3
        warnings.filterwarnings('error')

    for i in ignored_warnings:
        warnings.filterwarnings('ignore', message=fr"[\s\S]*{i}*")

    for i in ignored_warnings_module_category:
        warnings.filterwarnings('ignore', module=i[0], category=i[1])


def info(message, caption="User message"):
    log_warn(return_str(message, caption=caption, objectize=False), log_type='INFO')


def warn(message, caption="User message"):
    """Raise warning - just message, not traceback. Can be colorized. Display of warning is based on warning settings.
    You can configure how to cope with warnings with function set_warnings with debug parameter. Instead of traceback_warning
    this is not from catched error. It usually bring some information good to know.

    Args:
        message (str): Any string content of warning.
        caption (ctr): Headning of warning.
    """

    log_warn(return_str(message, caption=caption, objectize=False), log_type='USER WARNING')


def traceback(message=None, caption='Traceback warning'):
    """Raise warning with current traceback as content. It means, that error was catched, but still something crashed.

    Args:
        caption (str, optional): Caption of warning. Defaults to 'Traceback warning'.
    """
    if config.COLOR in [True, 1] or (config.COLOR == 'auto' and (not config.TO_FILE)):
        separated_traceback = pygments.highlight(trcbck.format_exc(), PythonTracebackLexer(), TerminalFormatter(style='friendly'))
    else:
        separated_traceback = trcbck.format_exc()

    separated_traceback = return_str(message=f"{message}\n\n{separated_traceback}", caption=caption, objectize=False)

    log_warn(separated_traceback, log_type='TRACEBACK WARNING')


def return_str(message, caption="User message", around='config', objectize=True):
    """Return enhanced colored message. Used for raising exceptions, assertions.

    Args:
        message (str): Any string content of warning.
        caption (ctr, optional): Headning of warning. Defaults to 'Traceback message'.
        around (bool, optional): If print to file - whether print ====== lines around.
            If 'config', use global config. Defaults to 'config'.
        objectize (bool, optional): Turn into object (If call in raise - only way to print colors).
            If you need string to variable, call str(). Defaults to True.

    Returns:
        str: Enhanced message as a string, that is wrapped by and can be colorized.
    """

    around = True if not config.TO_FILE else config.AROUND

    if around:
        bottom_line = colorize(f"\n\n{'=' * (len(caption) + 20)}\n\n")
        updated_str = (
            f"\n\n\n========= {caption} ========="
            f"\n\n{message}"
            f"{bottom_line}")
    else:
        updated_str = f"{caption}: {message}\n"

    updated_str = textwrap.indent(text=updated_str, prefix='    ')

    updated_str = colorize(updated_str)

    if objectize:
        updated_str = objectize_str(updated_str)

    return updated_str
