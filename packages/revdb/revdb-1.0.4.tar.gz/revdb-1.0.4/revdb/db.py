import copy
import time
import uuid
from functools import partial
from typing import Any, Dict, Type, TypeVar

import requests
from bson.objectid import ObjectId
from mongoengine import Document, DynamicDocument, IntField, ObjectIdField, StringField
from mongoengine import connect as mongo_connect  # ignore: type
from mongoengine.base import BaseDocument
from pymongo import MongoClient
from typing_extensions import Protocol

URLS_V1 = {
    "stg": "https://jstorage-stg.revtel-api.com/v1",
    "prod": "https://jstorage.revtel-api.com/v1",
}

_db_hosts: Dict[str, Any] = {}


def default_timestamp() -> int:
    return int(time.time())


def _get_v1_host(stage: str) -> str:
    try:
        return URLS_V1[stage]
    except KeyError as exc:
        raise ValueError("stage should be in [stg, prod]") from exc


def connect(
    client_id: str, client_secret: str, stage: str = "stg", alias: str = "default"
) -> MongoClient:
    host = _get_v1_host(stage)
    key = f"{client_id}__{alias}"

    try:
        db = _db_hosts[key]
    except KeyError:
        full_url = (
            f"{host}/settings?client_secret={client_secret}&client_id={client_id}"
        )
        resp = requests.get(full_url)
        resp.raise_for_status()

        resp_json = resp.json()
        db = mongo_connect(
            resp_json["client_id"], host=resp_json["db_host"], alias=alias
        )
        _db_hosts[key] = db

    return db


DOC = TypeVar("DOC", bound=BaseDocument)


def from_collection(
    client_id: str,
    client_secret: str,
    collection: str,
    stage: str = "stg",
    alias: str = "default",
) -> Type[BaseDocument]:
    def save_with_updated(self: BaseDocument, *args: Any, **kwargs: Any) -> Any:
        setattr(self, "updated", default_timestamp())
        return DynamicDocument.save(self, *args, **kwargs)

    host = _get_v1_host(stage)
    url = f"{host}/collection/{collection}?client_id={client_id}&client_secret={client_secret}"

    alias = f"{client_id}__{alias}"

    resp = requests.get(url)
    resp.raise_for_status()
    resp_json = resp.json()

    connect(client_id, client_secret, stage=stage, alias=alias)

    namespace = {
        "meta": {"collection": collection, "db_alias": alias, "id_field": "_obj_id"},
        resp_json["primary_key"]: StringField(
            unique=True, default=uuid.uuid4().__str__()
        ),
        "_obj_id": ObjectIdField(default=ObjectId, primary_key=True),
        "created": IntField(default=default_timestamp),
        "updated": IntField(default=default_timestamp),
        "save": save_with_updated,
    }
    return type(f"{client_id}__{collection}", (DynamicDocument,), namespace)


class FactoryProtocol(Protocol):
    def __call__(
        self, collection: str, alias: str = "default"
    ) -> Type[DynamicDocument]:
        pass  # pragma: no cover


def collection_factory(
    client_secret: str, client_id: str, stage: str = "stg"
) -> FactoryProtocol:
    return partial(
        from_collection, client_id=client_id, client_secret=client_secret, stage=stage
    )


def make_model_class(base: Type[DOC], **meta: Any) -> Type[DOC]:
    return type(base.__name__, (base,), {"meta": meta})


def create_connected_model(
    doc_class: BaseDocument, client_id: str, host: str, **kwargs: Any
) -> BaseDocument:
    db = client_id
    alias = f"{db}_alias"

    copy_class = copy.deepcopy(doc_class)
    copy_class.__name__ = f"{db}__{doc_class.__name__}"

    mongo_connect(db, host=host, alias=alias)
    return make_model_class(copy_class, db_alias=alias, **kwargs)


class ModelMixin:
    _meta: Dict[str, Any]

    @classmethod
    def from_client(cls, client_id: str) -> BaseDocument:
        db_host = cls._meta.get("db_host")
        if not db_host:
            raise ValueError("should define db_host in meta")

        return create_connected_model(
            cls,
            host=db_host,
            client_id=client_id,
        )


class Model(ModelMixin, DynamicDocument):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}


class StrictModel(ModelMixin, Document):  # type: ignore
    meta: Dict[str, Any] = {"abstract": True}
