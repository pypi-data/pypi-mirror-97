from unittest.mock import patch

from mongoengine import DynamicDocument, IntField, ObjectIdField, StringField
from mongoengine import connect as mongo_connect
from mongoengine.connection import _get_db

from revdb import Model, collection_factory, connect, make_model_class

PATCH_PATH = "requests.get"


class DocumentBase(DynamicDocument):  # type: ignore
    meta = {"abstract": True}


def test_make() -> None:
    child_doc = make_model_class(
        DocumentBase, db_alias="child_alias", collection="child_collection"
    )
    mongo_connect("child_db", host="server.example.com", alias="child_alias")
    assert issubclass(child_doc, DocumentBase)
    assert child_doc._get_collection_name() == "child_collection"
    assert child_doc._get_db().name == "child_db"


def test_connect() -> None:
    with patch(PATCH_PATH) as requests:
        requests.return_value.json.return_value = {
            "client_id": "test-id",
            "db_host": "fakehost.com",
        }
        connect(client_id="test-id", client_secret="testkey", alias="test_host")

        assert _get_db("test_host").name == "test-id"

        try:
            connect(
                client_id="test-id",
                client_secret="testkey",
                alias="test_host",
                stage="error_stage",
            )
        except ValueError as e:
            assert str(e) == "stage should be in [stg, prod]"


class BasicModel(Model):
    meta = {"abstract": True, "db_host": "foo"}


class NonHostModel(Model):
    meta = {"abstract": True}


def test_model() -> None:
    connected_model = BasicModel.from_client(client_id="test")

    assert connected_model.__name__ == BasicModel.__name__
    assert issubclass(connected_model, BasicModel)

    db = connected_model._get_db()

    assert db.name == "test"

    try:
        NonHostModel.from_client(client_id="non_host")
    except ValueError as exc:
        assert str(exc) == "should define db_host in meta"


def test_colleciton_factory() -> None:
    factory = collection_factory(client_id="test-id", client_secret="test_secret")

    with patch(PATCH_PATH) as requests:
        requests.return_value.json.return_value = {
            "client_id": "test-id",
            "name": "test-col",
            "primary_key": "id",
            "db_host": "fake-host",
        }

        doc_class = factory(collection="test-col", alias="test-alias")
        meta = doc_class._meta
        assert doc_class.__name__ == "test-id__test-col"
        assert meta["collection"] == "test-col"
        assert meta["db_alias"] == "test-id__test-alias"
        assert issubclass(doc_class, DynamicDocument)
        assert isinstance(doc_class.id, StringField)
        assert isinstance(doc_class._obj_id, ObjectIdField)
        assert isinstance(doc_class.created, IntField)
        assert isinstance(doc_class.updated, IntField)

        with patch("revdb.db.DynamicDocument.save") as save:
            save.return_value = {}
            doc = doc_class(id="test-id")
            with patch("revdb.db.default_timestamp") as dstamp:
                dstamp.return_value = doc.created + 1
                doc.save()
            assert doc.updated > doc.created
