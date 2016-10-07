import functools

from flask import jsonify, request, url_for


def no_resource_error_handler(f):
    """Error handler if resouce does not exist.

    The output of this decorator is either the results of the route
    if the resource exists or an error message if the resource does
    not exist.
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            results = f(*args, **kwargs)
        except AttributeError:
            return jsonify({'error': 'resource does not exist'})

        return results
    return wrapped


def paginate(collection, page=1, limit=25):
    """Generate a paginated response for a resource collection.

    Routes that use this decorator must return a SQLAlchemy query as a
    response.

    The output of this decorator is a json response with the paginated
    results.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            query = f(*args, **kwargs)

            requested_limit = request.args.get('limit', type=int, default=limit)
            requested_page = request.args.get('page', type=int, default=page)

            items = [item.to_dict() for item in query.paginate(page=requested_page,
                                                               per_page=requested_limit).items]

            response = {
                collection: items,
                'next': url_for(request.endpoint, limit=limit, page=page+1, _external=True),
                'total': query.count()
            }
            return jsonify(response)
        return wrapped
    return decorator
