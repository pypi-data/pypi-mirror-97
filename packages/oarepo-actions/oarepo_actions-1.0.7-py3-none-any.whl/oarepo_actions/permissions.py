from functools import wraps

from flask import abort, request
from invenio_records_rest import current_records_rest


def action_need_record_permission(factory_name):
    """Decorator checking that the user has the required permissions on record.

    :param factory_name: name of the permission factory.
    """
    def need_record_permission_builder(f):
        @wraps(f)
        def need_record_permission_decorator(self, record=None, *args,
                                             **kwargs):
            permission_factory = (
                getattr(self, factory_name) or
                getattr(current_records_rest, factory_name)
            )

            # FIXME use context instead
            request._methodview = self

            if permission_factory:
                actions_verify_record_permission(permission_factory, record, *args, **kwargs)
            return f(self, record=record, *args, **kwargs)
        return need_record_permission_decorator
    return need_record_permission_builder

def actions_verify_record_permission(permission_factory, record, *args, **kwargs):
    if not permission_factory(record=record, *args, **kwargs).can():
        from flask_login import current_user
        if not current_user.is_authenticated:
            abort(401)
        abort(403)
