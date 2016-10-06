import functools

from flask import jsonify


def no_resource_error_handler(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            results = f(*args, **kwargs)
        except AttributeError:
            return jsonify({'error': 'resource does not exist'})

        return results
    return wrapped
