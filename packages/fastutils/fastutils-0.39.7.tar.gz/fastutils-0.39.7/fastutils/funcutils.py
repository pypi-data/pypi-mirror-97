# -*- coding: utf-8 -*-
import time
import functools
import logging
from inspect import signature

import bizerror

from . import typingutils


logger = logging.getLogger(__name__)

def get_default_values(func):
    data = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default != parameter.empty:
            data[name] = parameter.default
    return data

def get_inject_params(func, data):
    params = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default is parameter.empty: # no default value, this parameter is required
            if not name in data:
                raise bizerror.MissingParameter("Missing required parameter: {0}".format(name))
            value = data[name]
        else:
            value = data.get(name, parameter.default)
        if not parameter.annotation is parameter.empty:
            value = typingutils.smart_cast(parameter.annotation, value, field_name=name)
        params[name] = value
    return params

def call_with_inject(func, data):
    params = get_inject_params(func, data)
    return func(**params)

def mcall_with_inject(funcs, data):
    if not isinstance(funcs, (list, set, tuple)):
        funcs = [funcs]
    results = []
    for func in funcs:
        params = get_inject_params(func, data)
        result = func(**params)
        results.append(result)
    return results

class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class chain(object):
    def __init__(self, *args):
        self.funcs = args
    
    def __call__(self, init_result, extra_args=None, extra_kwargs=None):
        extra_args = extra_args or []
        extra_kwargs = extra_kwargs or {}
        result = init_result
        for func in self.funcs:
            if func and callable(func):
                result = func(result, *extra_args, **extra_kwargs)
        return result


class BunchCallable(object):

    def __init__(self, *args, return_callback_results=False):
        self.return_callback_results = return_callback_results
        self.funcs = []
        for func in args:
            if isinstance(func, self.__class__):
                self.funcs += func.funcs
            else:
                self.funcs.append(func)

    def __call__(self, *args, **kwargs):
        results = []
        for func in self.funcs:
            if func and callable(func):
                result = func(*args, **kwargs)
            else:
                result = None
            results.append(result)
        if self.return_callback_results:
            return results
        else:
            return None


def try_again_on_error(sleep: int=5, limit: int=0, callback=None, callback_args=None, callback_kwargs=None):
    def outter_wrapper(func):
        def wrapper(*args, **kwargs):
            counter = 0
            while True:
                counter += 1
                try:
                    return func(*args, **kwargs)
                except InterruptedError:
                    logger.info("exit on got InterruptedError...")
                    break
                except Exception as error:
                    logger.exception("got unknown exception: {0}".format(str(error)))
                    if callback:
                        logger.info("call callback function {0} with params {1} {2}".format(str(callback), str(callback_args), str(callback_kwargs)))
                        local_callback_args = callback_args or []
                        local_callback_kwargs = callback_kwargs or {}
                        callback(*local_callback_args, **local_callback_kwargs)
                    time.sleep(sleep)
                if limit and counter >= limit:
                    break
        return functools.wraps(func)(wrapper)
    return outter_wrapper
