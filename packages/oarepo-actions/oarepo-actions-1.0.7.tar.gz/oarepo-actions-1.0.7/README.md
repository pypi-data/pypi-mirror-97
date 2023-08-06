OARepo-actions
==============

[![image][]][1]
[![image][2]][3]
[![image][4]][5]
[![image][6]][7]

Instalation
----------
```bash
    pip install oarepo-actions
```
Usage
----------
The library provides functionality for adding functions into your data models with supported REST methods, which are GET, POST, PUT and DELETE.
It will create URL rule for your method, and use default or defined serializers, permissions and url path.

Decorate your method with ```@action()``` decorator and add optional parameters. You must have ``**kwargs`` as your function parameter.

### List of optional parameters
###### url_path: 
- for specifing url_path, which will be added after ```list-route``` or ```item-route``` from your configuration
###### permissions:
- by default ```allow all```
- accepts permission factory
###### method:
- for REST method
- by default ```get```
- you can use ```get```, ```put```, ```delete``` or ```post``` written with lowercase letters
###### serializers:
- by default `application/json` serializer. 
- accepts dictionary where key is MIME type and value your own serializer
- serializers takes arguments from function as *args.Therefore if you want to return array, you must
wrap it with another array ( ```return [["a", "b", "c"]]``` )
###### detail: 
- by default ```True```. Change to ```False``` if method is class method
- determines which route will be used (```list route``` if detail is False)

Examples
--------
```python
class SampleRecord(Record):

    @action()
    def test_a(self, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(detail=False, url_path="send_email")
    def test_b(cls, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(detail=False, permissions=permission_factory)
    def test_c(cls, **kwargs):
        return {"title": self["title"]}

    @classmethod
    @action(detail=False, url_path="test/<int:param>",  permissions=permission_factory)
    def test_d(cls, param = None, **kwargs):
        print("jej")
        return Response(status=200)

    @classmethod
    @action(detail=False, permissions = permission_factory, serializers = {'text/html': make_response})
    def test_e(cls, **kwargs):
        return '<h1>xx</h1>'

    @classmethod
    @action(detail=False, url_path='test',permissions=allow_all, method='post')
    def test_f(cls, param=None, **kwargs):
        return {param: "yy"}

```
- url_a = ```server```/records/1/test_a
- url_b = ```server```/records/send_email
- url_c = ```server```/records/test_c
- url_d = ```server```/records/test/42
- url_e = ```server```/records/test_e
- url_f = ```server```/records/test
    - post method

### Record class
If you put ``record_class`` parameter in your decorated function, it will be filled with record class obtained from config.py

#### Example
```python
    @classmethod
    @action(detail=False, url_path="jej")
    def test(cls,record_class, **kwargs):
        record_uuid = uuid.uuid4()
        data = {"title": "The title of the record", "contributors": [{"name": "something"}]}
        pid, data = record_minter(record_uuid, data)
        record = record_class.create(data=data, id_=record_uuid)
        indexer = RecordIndexer()
        res = indexer.index(record)
        db.session.commit()
        return record

```

  [image]: https://img.shields.io/travis/oarepo-actions/oarepo-actions.svg
  [1]: https://travis-ci.org/oarepo/oarepo-actions
  [2]: https://img.shields.io/coveralls/oarepo/oarepo-actions.svg
  [3]: https://coveralls.io/r/oarepo/oarepo-actions
  [4]: https://img.shields.io/github/license/oarepo/oarepo-actions.svg
  [5]: https://github.com/oarepo/oarepo-actions/blob/master/LICENSE
  [6]: https://img.shields.io/pypi/v/oarepo-actions.svg
  [7]: https://pypi.org/pypi/oarepo-actions