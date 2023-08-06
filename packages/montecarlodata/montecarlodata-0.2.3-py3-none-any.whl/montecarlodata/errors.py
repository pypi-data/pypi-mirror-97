import traceback
from typing import Any, Optional, List

import click
from functools import wraps

import montecarlodata.settings as settings


def manage_errors(func):
    """
    Convenience decorator to abort on any errors after logging based on verbosity settings

    Requires an `_abort_on_error` field to be set in the instance
    """

    @wraps(func)
    def _impl(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except click.Abort:
            raise click.Abort()  # re-raise to prevent swallowing
        except Exception as error:
            echo_error(error, [traceback.format_exc()])

        if hasattr(self, '_abort_on_error') and self._abort_on_error:
            raise click.Abort()

    return _impl


def echo_error(message: Any, errors: Optional[List[Any]] = None) -> None:
    """
    Convenience utility to echo any error in verbose and quiet mode
    """
    click.echo(f'Error - {message}')
    if settings.MCD_VERBOSE_ERRORS:
        for error in errors or []:
            click.echo(error)


def complain_and_abort(message: str) -> None:
    """
    Convenience utility to echo message and exit
    """
    click.echo(f'Error - {message}')
    raise click.Abort()
