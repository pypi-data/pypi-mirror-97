""" Test module. Auto pytest that can be started in IDE or with

    >>> python -m pytest

in terminal in tests folder.
"""
#%%

import sys
from pathlib import Path
import inspect
import os
import warnings
import io

tests_path = Path(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)).parent
root_path = tests_path.parent

for i in [tests_path, root_path]:
    if i.as_posix() not in sys.path:
        sys.path.insert(0, i.as_posix())

from help_file import info_outside, warn_outside, traceback_outside
import mylogging


# Basic use cases testing
def test_readme():
    import mylogging

    mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    # We can log / warn tracebacks from expected errors and continue runtime.

    try:
        print(10 / 0)

    except ZeroDivisionError:
        mylogging.traceback("Maybe try to use something different than 0.")

    # Info will not trigger warning, but just print to console (but follows the rule in set_warnings(debug)).

    mylogging.info("I am interesting info")


def test_readme_to_file():

    import mylogging

    mylogging.config.TO_FILE = "log.log"  # You can use relative (just log.log)

    # Then it's the same

    mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    try:
        print(10 / 0)
    except ZeroDivisionError:
        mylogging.traceback("Maybe try to use something different than 0.")

    mylogging.info("I am interesting info")

    mylogging.config.TO_FILE = False

    os.remove("log.log")


# Unit tests... test basic features


def test_readme_configs():
    import mylogging
    mylogging.config.COLOR = 0  # Turn off colorization on all functions to get rid of weird symbols

    mylogging.info('Not color')


def test_return_str():
    mylogging.config.COLOR = 1
    try:
        raise Exception(mylogging.return_str("asdas", caption="User"))
    except Exception:
        pass

    assert mylogging.return_str("asdas", caption="User")


def test_logs():

    mylogging.config.TO_FILE = "delete.log"

    errors = []

    def check_log():
        with open('delete.log') as log:
            log_content = log.read()

        os.remove('delete.log')

        if log_content:
            return True
        else:
            return False

    mylogging.info('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    if not check_log():
        errors.append('Info not created')


    mylogging.warn('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

    if not check_log():
        errors.append('Warning not created')

    try:
        print(10 / 0)

    except Exception:
        mylogging.traceback("Maybe try to use something different than 0")

    if not check_log():
        errors.append('Traceback not created')

    for i in [info_outside, warn_outside, traceback_outside]:
        i('Message')
        if not check_log():
            errors.append('Outside function not working')


def test_warnings():

    mylogging.config.TO_FILE = False

    errors = []

    def get_stdout(func, args=[], kwargs={}, loop=1):

        stdout = sys.stdout
        sys.stdout = io.StringIO()

        for i in range(loop):
            func(*args, **kwargs)

        output = sys.stdout.getvalue()
        sys.stdout = stdout

        return output


    ################
    ### Debug = 0 - show not
    ################

    with warnings.catch_warnings(record=True) as w:
        mylogging.set_warnings(debug=0)

        if get_stdout(mylogging.info, ['Hello']):
            errors.append('Info printed, but should not.')

        mylogging.warn('asdasd')

        try:
            print(10 / 0)

        except Exception:
            mylogging.traceback("Maybe try to use something different than 0")

        if w:
            errors.append('Warn, but should not.')

    ################
    ### Debug = 1 - show once
    ################

    with warnings.catch_warnings(record=True) as w:
        mylogging.set_warnings(debug=1)

        output = get_stdout(mylogging.info, ['Hello'], loop=2)

        if not output:
            errors.append('Info not printed, but should.')

        outuput_lines_count = len(output.splitlines())

        mylogging.warn('asdasd')
        mylogging.warn('dva')
        mylogging.warn('asdasd')

        try:
            print(10 / 0)

        except Exception:
            mylogging.traceback("Maybe try to use something different than 0")

        if len(w) != 3:
            errors.append("Doesn't warn once.")

    ################
    ### Debug = 2 - show always
    ################

    with warnings.catch_warnings(record=True) as w:
        mylogging.set_warnings(debug=2)

        mylogging.warn('asdasd')
        mylogging.warn('asdasd')

        if len(w) != 2:
            errors.append("Doesn'twarn always.")

        outuput_always = get_stdout(mylogging.info, ['Hello'], loop=2)
        outuput_lines_count_always = len(outuput_always.splitlines())

        if outuput_lines_count_always <= outuput_lines_count:
            errors.append("Info printed always if shouldn'r or vice versa.")

    ################
    ### Debug = 3 - Stop on error
    ################

    mylogging.set_warnings(debug=3)

    try:
        errors.append('Not stopped on runtime warning.')
        mylogging.warn('asdasd')
    except Exception:
        errors.pop()

    try:
        errors.append('Not stopped on traceback warning')

        try:
            print(10 / 0)

        except Exception:
            mylogging.traceback("Maybe try to use something different than 0")

    except Exception:
        errors.pop()

    # Test outer file
    with warnings.catch_warnings(record=True) as w:
        mylogging.set_warnings(1)

        if not get_stdout(info_outside, ['Message']):
            errors.append('Outside info not working')

        warn_outside('Message')
        traceback_outside('Message')

        if len(w) != 2:
            errors.append('Warn from other file not working')

    assert not errors


# def test_settings():
#     # TODO
#     # Test color and debug
#     pass


if __name__ == "__main__":
    # test_readme()
    # test_readme_to_file()
    # test_return_str()
    # test_readme_configs()
    pass
