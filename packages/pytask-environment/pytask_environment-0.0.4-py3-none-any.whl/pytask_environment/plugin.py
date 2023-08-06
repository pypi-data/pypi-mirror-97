"""Entry-point for the plugin."""
from _pytask.config import hookimpl
from pytask_environment import collect
from pytask_environment import database


@hookimpl
def pytask_add_hooks(pm):
    """Register some plugins."""
    pm.register(collect)
    pm.register(database)
