import inspect
import json
from collections import defaultdict

import invenio_base
from deepmerge import always_merger
from flask import Blueprint, abort, current_app, make_response, url_for
from invenio_app.helpers import obj_or_import_string
from invenio_base.signals import app_loaded
from invenio_records_rest.utils import allow_all

from .record_action import RecordAction
from .record_action_list import RecordActionList


def make_json_response(data):
    response = current_app.response_class(
        json.dumps(data),
        mimetype='application/json')
    response.status_code = 200

    return response

default_serializer = {'GET': {'application/json': make_json_response}, 'POST': {'application/json': make_json_response}}


# todo permissions
def url_helper(meths):
    no_rule = True
    route_rule = str()
    method = {}
    permissions = allow_all
    serializers_list = []
    serializers = {}
    detail = True
    for l in meths:
        if no_rule:
            if 'detail' in l[2]:
                pom = l[3]
                route_rule = pom['list_route'] + str(l[0])
                no_rule = False
                detail = False
            else:
                pom = l[3]
                route_rule = pom['item_route'] + str(l[0])
                no_rule = False
        method.update({l[1]: l[4]})
        try:
            serializers_list.append(l[3]['serializers'])
        except:
            pass
    if len(serializers_list) == 0:
        serializers = default_serializer
    else:
        for i in serializers_list:
            always_merger.merge(serializers, i)

    return route_rule, method, permissions, serializers, detail


def agg_url_path(record_class):
    list_endpoints = defaultdict(dict)
    item_endpoints = defaultdict(dict)

    for action in extract_actions(record_class):
        if action['detail']:
            item_endpoints[action['url_path']][action['method']] = action
        else:
            list_endpoints[action['url_path']][action['method']] = action


def create_route(path, action):
    if path.endswith('/'):
        return path + action['url_path']
    else:
        return path + '/' + action['url_path']


def get_record_class(endpoint_configuration):
    if 'record_class' not in endpoint_configuration:
        return
    record_class = endpoint_configuration['record_class']
    record_class = obj_or_import_string(record_class)
    return record_class


def extract_actions(record_class):
    for name, function in inspect.getmembers(record_class):
        if hasattr(function, '__action'):
            attribut_content = getattr(function, '__action')
            yield attribut_content


def register_blueprints(blueprint, record_class, endpoint, endpoint_configuration):
    for action in extract_actions(record_class):
        if not action['detail']:
            blueprint.add_url_rule(create_route(endpoint_configuration['list_route'], action),
                                   view_func=RecordActionList.as_view(
                                       RecordActionList.view_name.format(endpoint, action["function_name"]),
                                       permissions=action['permissions'], serializers=action['serializers'],
                                       record_class=record_class, function_name=action['function_name']),
                                   methods=[action['method']])
        else:
            blueprint.add_url_rule(create_route(endpoint_configuration['item_route'], action),
                                   view_func=RecordAction.as_view(
                                       RecordAction.view_name.format(endpoint, action["function_name"]),
                                       permissions=action['permissions'], serializers=action['serializers'],
                                       function_name=action['function_name']), methods=[action['method']])


def action_urls(sender, app=None, **kwargs):
    with app.app_context():
        actions = Blueprint("oarepo_actions", __name__, url_prefix=None, )
        rest_endpoints = app.config["RECORDS_REST_ENDPOINTS"]
        for endpoint, configuration in rest_endpoints.items():
            record_class = get_record_class(configuration)
            if not record_class:
                continue
            register_blueprints(actions, record_class, endpoint, configuration)
        app.register_blueprint(actions)


class Actions(object):
    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""

        app.extensions['testinvenio-oarepo_actions'] = self
        app_loaded.connect(action_urls)
