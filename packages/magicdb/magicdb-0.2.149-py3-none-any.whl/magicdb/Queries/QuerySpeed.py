import typing as T
from typing import Union, List
import magicdb
from magicdb import db, ASCENDING, DESCENDING, DocumentSnapshot
from magicdb.Queries.Q import Q
from magicdb.utils.Serverless.span import safe_span
from magicdb.utils.async_helpers import magic_async

import redis

import ujson

import time


class QuerySpeed:
    def __init__(self, cls):
        from magicdb.Models.MagicModelSpeed import MagicModelSpeed

        self.cls: MagicModelSpeed = cls
        self.collection_path = self.cls.get_collection_name()
        self.firebase_query = self.create_query()
        self.query_inputs: List[str] = []

    @property
    def key(self):
        return self.get_path_of_query()

    def create_query(self):
        self.firebase_query = db.conn.collection(self.collection_path)
        return self.firebase_query

    def parent(self, parent_or_path):
        from magicdb.Models.MagicModelSpeed import MagicModelSpeed

        parent_path = (
            parent_or_path
            if not issubclass(type(parent_or_path), MagicModelSpeed)
            else parent_or_path._key
        )

        self.collection_path = parent_path + "/" + self.collection_path
        self.create_query()
        return self

    def document(self, document_path):
        self.firebase_query = self.firebase_query.document(document_path)
        return self

    def collection_group(self):
        self.firebase_query = db.conn.collection_group(self.cls.get_collection_name())
        return self

    def collection(self, collection_path):
        self.firebase_query = self.firebase_query.collection(collection_path)
        return self

    """Wrapping Firestore abilities."""

    def where(self, field, action, value):
        self.firebase_query = self.firebase_query.where(field, action, value)
        self.query_inputs.append(f"{field}, {action}, {value}")
        return self

    def order_by(self, field, direction=None, **kwargs):
        if direction:
            kwargs["direction"] = direction
        if kwargs.get("direction", None) == "asc":
            kwargs["direction"] = ASCENDING
        if kwargs.get("direction", None) == "desc":
            kwargs["direction"] = DESCENDING
        self.firebase_query = self.firebase_query.order_by(field, **kwargs)
        return self

    def start_at(self, fields):
        self.firebase_query = self.firebase_query.start_at(fields)
        return self

    def start_after_id(self, last_doc_id: str = None):
        if not last_doc_id:
            return self
        key = self.cls.construct(id=last_doc_id)._key
        snapshot = db.conn.document(key).get()
        self.firebase_query = self.firebase_query.start_after(snapshot)
        return self

    def start_after(self, fields):
        self.firebase_query = self.firebase_query.start_after(fields)
        return self

    def end_at(self, fields):
        self.firebase_query = self.firebase_query.end_at(fields)
        return self

    def end_before(self, fields):
        self.firebase_query = self.firebase_query.end_before(fields)
        return self

    def limit(self, limit):
        print("calling limit", limit)
        if not limit or limit == -1:
            return self
        self.firebase_query = self.firebase_query.limit(limit)
        return self

    def add_q(self, q: Q = None):
        if not q:
            return self
        self.limit(q.limit)
        self.start_after_id(q.start_after_id)
        return self

    def get_path_of_query_old(self):
        if getattr(self.firebase_query, "_path", None):
            return "/".join(self.firebase_query._path)
        if getattr(self.firebase_query, "_parent", None):
            return "/".join(self.firebase_query._parent._path)
        else:
            return self.collection_path

    def get_path_of_query(self):
        if path := getattr(self.firebase_query, "path", None):
            return path
        if parent := getattr(self.firebase_query, "_parent", None):
            return "/".join(parent._path)
            # return parent.path
        else:
            return self.collection_path

    """Querying and creating of the models."""

    def make_safe_span_label(self, query_type):
        return f"{query_type}-{self.get_path_of_query()}-{str(self.query_inputs)}"

    @magic_async
    def stream(self, validate_db_data=True, **kwargs):
        """Currently defaults to validating the db data, but you can turn this off with the validate_db_data param"""
        with safe_span(self.make_safe_span_label("stream")):
            docs = list(self.firebase_query.stream(**kwargs))

        constructor = self.cls if validate_db_data else self.cls.construct

        return [
            constructor(
                from_db=True, _doc=doc, **doc.to_dict(), _key=doc.reference.path
            )
            for doc in docs
        ]

    """START OF EDITED PART"""

    def model_from_dict(
        self,
        *,
        d: T.Optional[dict],
        key: str = None,
        doc: magicdb.DocumentSnapshot = None,
        create: bool = False,
        validate_db_data: bool = True,
    ):

        _key = self.key if not key else key

        if not d:
            return None if not create else self.cls(_key.split("/")[-1])

        constructor = self.cls if validate_db_data else self.cls.construct

        return constructor(
            from_db=True,
            _doc=doc,
            **d,
            _key=_key,
        )

    def d_from_firestore(self, **kwargs) -> T.Optional[dict]:
        with safe_span(self.make_safe_span_label("get")):
            doc = self.firebase_query.get(**kwargs)

        if type(doc) != DocumentSnapshot:
            return None

        with safe_span("to_dict"):
            return doc.to_dict()

    def model_mapping_from_firestore(
        self, refs: List[magicdb.DocumentReference], **kwargs
    ) -> T.Dict[str, dict]:
        with safe_span(self.make_safe_span_label("get_all")):
            docs = list(db.conn.get_all(refs, **kwargs))
        with safe_span(self.make_safe_span_label(f"to_dict {len(docs)=}")):
            return {doc.reference.path: doc.to_dict() for doc in docs}

    def model_mapping_from_redis(
        self, keys: List[str]
    ) -> T.Optional[T.Dict[str, dict]]:
        if not self.r:
            return None
        raw_strs = self.r.mget(keys)
        mapping = {}
        with safe_span(self.make_safe_span_label("*ujson.loads-from mget*")):
            for key, raw_str in zip(keys, raw_strs):
                value = None if raw_str is None else ujson.loads(raw_str)
                mapping[key] = value
        return mapping

    def d_from_redis(self) -> T.Optional[dict]:
        if not self.r:
            return None
        raw_str = self.r.get(self.key)
        if not raw_str:
            return None

        with safe_span(self.make_safe_span_label("*ujson.loads*")):
            return ujson.loads(raw_str)

    def model_mapping_to_redis(self, mapping: T.Dict[str, dict]) -> None:
        if not self.r:
            return None

        json_mapping = {}
        to_delete = []
        with safe_span(
            self.make_safe_span_label(f"construct-from-getall-miss:{self.cls.__name__}")
        ):
            for key, d in mapping.items():
                if not d:
                    to_delete.append(key)
                    continue
                model = self.cls.construct(**d)
                value = model.json(exclude_unset=True, exclude={"id"})
                json_mapping[key] = value
        if json_mapping:
            self.r.mset(json_mapping)
            if self.r_ttl_secs:
                with self.r.pipeline() as pipe:
                    for key in json_mapping.keys():
                        pipe.expire(key, self.r_ttl_secs)
                    pipe.execute()
        if to_delete:
            self.r.delete(*to_delete)

    def d_to_redis(self, d: dict) -> None:
        if not self.r or not d:
            return
        with safe_span(
            self.make_safe_span_label(f"construct-from-miss:{self.cls.__name__}")
        ):
            j = self.cls.construct(**d, _key=self.key).json(
                exclude_unset=True, exclude={"id", "_key"}
            )

        self.r.set(self.key, j, ex=self.r_ttl_secs)

    def get_mapping_from_db(
        self, ids: List[str], use_cache: bool = True, **kwargs
    ) -> T.Dict[str, dict]:
        refs = [db.conn.collection(self.collection_path).document(id) for id in ids]
        keys = [ref.path for ref in refs]

        model_mapping = {"hi": None}

        if use_cache:
            model_mapping: T.Dict[str, dict] = self.model_mapping_from_redis(keys=keys)

        if not use_cache or not model_mapping or None in model_mapping.values():
            if self.r and use_cache:
                print("cache miss for get all")
            model_mapping = self.model_mapping_from_firestore(refs=refs, **kwargs)
            if use_cache:
                self.model_mapping_to_redis(mapping=model_mapping)
        return model_mapping

    def get_d_from_db(self, use_cache: bool = True, **kwargs) -> T.Optional[dict]:
        d = None
        if use_cache:
            d = self.d_from_redis()
        if not d:
            # cache miss so get from firestore
            if self.r and use_cache:
                print("cache miss")
            d = self.d_from_firestore(**kwargs)
            if use_cache:
                self.d_to_redis(d=d)
        return d

    def get_internal(
        self, use_cache: bool = True, create=False, validate_db_data=True, **kwargs
    ):
        d = self.get_d_from_db(use_cache=use_cache, **kwargs)

        return self.model_from_dict(
            d=d, create=create, validate_db_data=validate_db_data
        )

    @magic_async
    def get(
        self,
        id=None,
        use_cache: bool = True,
        create=False,
        validate_db_data=True,
        **kwargs,
    ):
        if id:
            self.firebase_query = self.firebase_query.document(id)

        return self.get_internal(
            use_cache=use_cache,
            create=create,
            validate_db_data=validate_db_data,
            **kwargs,
        )

    @magic_async
    def get_all(
        self, ids: List[str], use_cache: bool = True, validate_db_data=True, **kwargs
    ) -> list:
        mapping = self.get_mapping_from_db(ids=ids, use_cache=use_cache, **kwargs)

        with safe_span(self.make_safe_span_label("get_all-creating models")):
            models = [
                self.model_from_dict(
                    d=d, key=key, doc=None, validate_db_data=validate_db_data
                )
                for key, d in mapping.items()
            ]
        return self.sort_models_by_id_order(models, ids)

    @staticmethod
    def sort_models_by_id_order(models, ids):
        """Maintain order of return array"""
        sorted_models = [None] * len(ids)
        sort_key = {id: index for index, id in enumerate(ids)}
        for model in models:
            if model:
                sorted_models[sort_key[model.id]] = model
        return sorted_models

    """REDIS"""

    @property
    def r(self) -> T.Optional[redis.Redis]:
        return self.cls.get_redis()

    @property
    def r_ttl_secs(self) -> T.Optional[int]:
        return self.cls.get_redis_ttl_secs()

    """END OF EDITED PART"""

    """Subcollections"""

    def collections(self):
        return self.firebase_query.collections()

    def collections_names(self):
        return [coll.id for coll in self.firebase_query.collections()]
