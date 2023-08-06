import json

from flask import current_app
from invenio_records_rest.views import need_record_permission, pass_record
from invenio_rest import ContentNegotiatedMethodView

from .permissions import action_need_record_permission


class RecordActionList(ContentNegotiatedMethodView):
    view_name = '{0}_{1}'

    def __init__(self, permissions, serializers, function_name, record_class):
        super().__init__(
            serializers=serializers,
            default_media_type='application/json'
        )
        self.action_permission_factory = permissions
        self.record_class = record_class
        self.function_name = function_name

    @action_need_record_permission('action_permission_factory')
    def get(self, **kwargs):
        return getattr(self.record_class, self.function_name)(record_class = self.record_class, **kwargs)

    @action_need_record_permission('action_permission_factory')
    def put(self, **kwargs):
        return getattr(self.record_class, self.function_name)(record_class = self.record_class, **kwargs)

    @action_need_record_permission('action_permission_factory')
    def delete(self, **kwargs):
        return getattr(self.record_class, self.function_name)(record_class = self.record_class, **kwargs)

    @action_need_record_permission('action_permission_factory')
    def post(self, **kwargs):
        return getattr(self.record_class, self.function_name)(record_class = self.record_class, **kwargs)
