import json
from functools import wraps

from flask import abort, current_app, request
from invenio_records_rest import current_records_rest
from invenio_records_rest.utils import allow_all


def make_json_response(data):
    response = current_app.response_class(
        json.dumps(data),
        mimetype='application/json')
    response.status_code = 200

    return response

default_serializers = {'application/json' : make_json_response}

def action(**kwargs):
    def wrapper(function):
        function.__action = kwargs
        if 'detail' not in function.__action:
            function.__action['detail'] = True
        if 'permissions' not in function.__action:
            function.__action['permissions'] = allow_all
        if 'url_path' not in function.__action:
            function.__action.update({'url_path': function.__name__})
        else:
            function.__action['url_path'] = function.__action['url_path'].lstrip('/')
        if 'method' not in function.__action:
            function.__action['method'] = 'get'
        if 'serializers' not in function.__action:
            function.__action['serializers'] = default_serializers
        function.__action['function_name'] = function.__name__
        return function
    return wrapper

