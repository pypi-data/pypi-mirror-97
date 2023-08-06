import json

from flask import current_app
from invenio_records_rest.views import need_record_permission, pass_record
from invenio_rest import ContentNegotiatedMethodView


class RecordAction(ContentNegotiatedMethodView):
    view_name = '{0}_{1}'

    def __init__(self, permissions, serializers, function_name):
        super().__init__(
            serializers=serializers,
            default_media_type='application/json'
        )
        self.action_permission_factory = permissions
        self.function_name = function_name

    @pass_record
    @need_record_permission('action_permission_factory')
    def get(self, pid, record, **kwargs):
        return getattr(record, self.function_name)(**kwargs)

    @pass_record
    @need_record_permission('action_permission_factory')
    def put(self, pid, record, **kwargs):
        return getattr(record, self.function_name)(**kwargs)

    @pass_record
    @need_record_permission('action_permission_factory')
    def delete(self, pid, record, **kwargs):
        return getattr(record, self.function_name)(**kwargs)

    @pass_record
    @need_record_permission('action_permission_factory')
    def post(self, pid, record, **kwargs):
        return getattr(record, self.function_name)(**kwargs)
