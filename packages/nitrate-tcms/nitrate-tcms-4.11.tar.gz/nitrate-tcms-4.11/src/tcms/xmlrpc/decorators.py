# -*- coding: utf-8 -*-

import inspect
import logging

from functools import wraps

from django.conf import settings
from kobo.django.xmlrpc.models import XmlRpcLog


__all__ = ('log_call',)

logger = logging.getLogger('nitrate.xmlrpc')

if settings.DEBUG:
    # To avoid pollute XMLRPC logs with those generated during development
    def create_log(user, method, args):
        log_msg = 'user: {}, method: {}, args: {}'.format(
            user.username if hasattr(user, 'username') else user,
            method,
            args)
        logger.debug(log_msg)
else:
    create_log = XmlRpcLog.objects.create


def log_call(*args, **kwargs):
    """Log XMLRPC-specific invocations

    This is copied from kobo.django.xmlrpc.decorators to add custom abilities,
    so that we don't have to wait upstream to make the changes.

    Usage::

        from tcms.core.decorators import log_call
        @log_call(namespace='TestNamespace')
        def func(request):
            return None
    """
    namespace = kwargs.get('namespace', '')
    if namespace:
        namespace = namespace + '.'

    def decorator(function):
        argspec = inspect.getfullargspec(function)
        # Each XMLRPC method has an HttpRequest argument as the first one,
        # it'll be ignored in the log.
        arg_names = argspec.args[1:]

        @wraps(function)
        def _new_function(request, *args, **kwargs):
            try:
                known_args = list(zip(arg_names, args))
                unknown_args = list(enumerate(args[len(arg_names):]))
                keyword_args = [
                    (key, value) for key, value in kwargs.items()
                    if (key, value) not in known_args
                ]

                create_log(user=request.user,
                           method=f'{namespace}{function.__name__}',
                           args=str(known_args + unknown_args + keyword_args))
            except Exception:
                logger.exception(
                    f'Fail to log XMLRPC call on {function.__name__}')
            return function(request, *args, **kwargs)

        return _new_function

    return decorator
