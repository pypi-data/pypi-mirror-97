import uuid

from flask import make_response
from invenio_access.permissions import Permission, any_user, authenticated_user
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.providers.recordid import RecordIdProvider
from invenio_records.api import Record
from invenio_records_rest.utils import allow_all
from oarepo_validate import MarshmallowValidatedRecordMixin, SchemaKeepingRecordMixin

from oarepo_actions.decorators import action

from .constants import SAMPLE_ALLOWED_SCHEMAS, SAMPLE_PREFERRED_SCHEMA
from .marshmallow import SampleSchemaV1


def record_minter(object_uuid, data):

    # pid = PersistentIdentifier.create(
    #     pid_type='recid',
    #     pid_value="xxxx",
    #     object_uuid=object_uuid,
    # )
    provider = RecordIdProvider.create(
        object_type='rec',
        object_uuid=object_uuid,
    )
    data['id'] = provider.pid.pid_value

    return provider.pid, data
def neco():
    return {"xx": "yy"}
def pf(record = None):
    return Permission(any_user)
class SampleRecord(SchemaKeepingRecordMixin,
                   MarshmallowValidatedRecordMixin,
                   Record):
    ALLOWED_SCHEMAS = SAMPLE_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = SAMPLE_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = SampleSchemaV1

    @action(url_path="blah", permissions = allow_all)
    def send_email(self, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(detail=False, url_path="jej", permissions = allow_all)
    def blah1(cls, **kwargs):
        return neco()

    @classmethod
    @action(detail=False, permissions=pf)
    def blah(cls, **kwargs):
        return neco()

    @classmethod
    @action(detail=False, url_path='test', permissions=allow_all)
    def test3(cls,record_class, param=None, **kwargs):
        return {param: "yy"}

    @classmethod
    @action(detail=False, url_path='test',permissions=allow_all, method='post')
    def test2(cls, param=None, **kwargs):
        return {param: "yy"}

    @classmethod
    @action(detail=False, url_path='mine')
    def test321(cls, param=None, **kwargs):
        return ["kch", "ll"]

    @action(url_path="blahx", permissions=allow_all, method = 'post')
    def x(self, **kwargs):
        return {"title": self["title"]}

    @action(url_path="blahx", permissions=allow_all)
    def x2(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all, method='get')
    def b(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all,url_path = 'b', method='put')
    def b1(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all,url_path = 'b', method='delete')
    def b2(self, **kwargs):
        return {"title": self["title"]}

    @action(permissions=allow_all, url_path = 'b', method='post', serializers = {'application/json': make_response})
    def b3(self, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(permissions=allow_all, url_path='kch',detail=False, method='post')
    def test_record_class(cls, record_class, **kwargs):
        # record_uuid = uuid.uuid4()
        # data = {"title": "neco", "contributors": [{"name": "neco"}]}
        # pid, data = record_minter(record_uuid, data)
        # record = record_class.create(data=data, id_=record_uuid)
        # indexer = RecordIndexer()
        # res = indexer.index(record)
        print(record_class.__name__)
        return {}

    _schema = "sample/sample-v1.0.0.json"
    def validate(self, **kwargs):
        return super().validate(**kwargs)
