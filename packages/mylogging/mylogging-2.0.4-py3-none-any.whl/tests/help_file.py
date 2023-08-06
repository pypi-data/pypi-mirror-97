import mylogging


def warn_outside(message):
    mylogging.warn(message)


def traceback_outside(message):

    try:
        print(10 / 0)

    except Exception:
        mylogging.traceback("message")


def info_outside(message):
    mylogging.info(message)
