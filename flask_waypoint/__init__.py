"""Flask-Waypoint, Manage database connections on master/slave scenarios."""

from functools import wraps
from contextlib import contextmanager


# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
from sqlalchemy import create_engine
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

__version__ = '0.0.1'

engines = {}
BINGINDS = ['master', 'slave']

STACK_BIND_PROPERTY = 'waypoint_current_bind'


class FlaskWaypoint:

    def __init__(self, app, db, raise_when_not_binding=False, master_config_key='DB_MASTER_URI', slave_config_key='DB_SLAVE_URI'):
        self.init_app(app, db, raise_when_not_binding, master_config_key, slave_config_key)

    def init_app(self, app, db, raise_when_not_binding=False, master_config_key='DB_MASTER_URI', slave_config_key='DB_SLAVE_URI'):
        """Init Flask-Waypoint within the application."""
        engines[app] = {}
        engines[app]['master'] = create_engine(app.config[master_config_key])
        engines[app]['slave'] = create_engine(app.config[slave_config_key])

        def get_engine(app, bind=None):
            ctx = stack.top
            current_bind = getattr(ctx, STACK_BIND_PROPERTY, None)
            if current_bind is None:
                if raise_when_not_binding and ctx is not None:  # We should not raise when doing actions outside a flask request
                    raise NoBindingActiveError
                current_bind = 'master'
                app.logger.warn('Using database without binding to master or slave, fallbacking to master')
            return engines[app][current_bind]

        db.get_engine = get_engine


class NoBindingActiveError(Exception):
    def __init__(self):
        super(Exception, self).__init__('Trying to access database without binding to master or slave before')


class TwoBindingsOnSameRequestError(Exception):
    def __init__(self):
        super(Exception, self).__init__('Trying to create a second binding on the same request')


@contextmanager
def db_master():
    """Contect managet to run a block within the master database."""
    with db_bind('master'):
        yield


@contextmanager
def db_slave():
    """Contect managet to run a block within the slave database."""
    with db_bind('slave'):
        yield


@contextmanager
def db_bind(bind):
    """Context manager to run a block within a database binding."""
    if bind not in BINGINDS:
        raise Exception('Unknown database binding')
    ctx = stack.top
    if getattr(ctx, STACK_BIND_PROPERTY, False):
        raise TwoBindingsOnSameRequestError()

    setattr(ctx, STACK_BIND_PROPERTY, bind)
    yield


def with_master(fn):
    """Decorator to run a method on the master db binding."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with db_master():
            return fn(*args, **kwargs)
    return wrapper


def with_slave(fn):
    """Decorator to run a method on the slave db binding."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with db_slave():
            return fn(*args, **kwargs)
    return wrapper
