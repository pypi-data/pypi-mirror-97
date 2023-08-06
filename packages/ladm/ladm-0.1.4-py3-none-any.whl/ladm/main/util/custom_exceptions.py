import sys


class ExitCodeException(Exception):
    """
    Base class for all exceptions that set the exit code
    """
    def get_exit_code(self):
        """ Override in derived classes """
        return 1


def handle_uncaught_exception(exception_type, value, trace):
    old_hook(exception_type, value, trace)
    if isinstance(value, ExitCodeException):
        sys.exit(value.get_exit_code())


sys.excepthook, old_hook = handle_uncaught_exception, sys.excepthook


class LADMError(ExitCodeException):
    def get_exit_code(self):
        return 5
