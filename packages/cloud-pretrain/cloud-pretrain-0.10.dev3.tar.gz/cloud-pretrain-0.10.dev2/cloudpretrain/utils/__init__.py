# coding: utf8
from __future__ import print_function, absolute_import

import six


def to_str(*data_array):
    def _to_str(data):
        if isinstance(data, six.string_types):
            if six.PY2:
                if isinstance(data, str):
                    return data
                else:
                    return data.encode("utf8")
            else:
                if isinstance(data, str):
                    return data
                else:
                    return data.decode("utf8")
        if isinstance(data, list) or isinstance(data, tuple):
            return [_to_str(s) for s in data]
        if isinstance(data, dict):
            return {_to_str(k): _to_str(data[k]) for k in data}
        return data

    if len(data_array) == 1:
        return _to_str(data_array[0])
    else:
        return _to_str(data_array)


def args_to_str(func):
    """
    Compatible with py2.
    It is designed to deal with the problem that func doesn't accept unicode args while be called with unicode args.
    This decorator will convert the unicode args into str args, then the decorated function call is safe with unicode
    args.
    """

    def wrapper(*args, **kwargs):
        args = to_str(args)
        kwargs = to_str(kwargs)
        return func(*args, **kwargs)

    return wrapper
