import sys

import click
from _pytask.config import hookimpl
from _pytask.exceptions import CollectionError
from pony import orm
from pytask_environment.database import Environment


@hookimpl(trylast=True)
def pytask_log_session_header():
    """Use the entry-point to implement an early exit.

    The solution is hacky. Exploit the first entry-point in the build process after the
    database is created.

    Check if the version and path of the Python interpreter have changed and if so, ask
    the user whether she wants to proceed.

    """
    same_version, same_path = have_version_or_path_changed(
        "python", sys.version, sys.executable
    )
    if not same_version or not same_path:
        message = "\nYour Python environment seems to have changed."
        message += " The Python version has changed." if not same_version else ""
        message += (
            " The path to the Python executable has changed." if not same_path else ""
        )
        message += " Do you want to continue with the current environment?"

        if click.confirm(message):
            create_or_update_state("python", sys.version, sys.executable)
        else:
            raise CollectionError


@orm.db_session
def have_version_or_path_changed(name, version, path):
    """Return booleans indicating whether the version or path of a package changed."""
    try:
        package = Environment[name]
    except orm.ObjectNotFound:
        Environment(name=name, version=version, path=path)
        same_version = True
        same_path = True
    else:
        same_version = package.version == version
        same_path = package.path == path

    return same_version, same_path


@orm.db_session
def create_or_update_state(name, version, path):
    """Create or update a state."""
    try:
        package_in_db = Environment[name]
    except orm.ObjectNotFound:
        Environment(name=name, version=version, path=path)
    else:
        package_in_db.version = version
        package_in_db.path = path
