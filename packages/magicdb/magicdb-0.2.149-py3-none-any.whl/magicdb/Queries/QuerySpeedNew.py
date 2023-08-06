import typing as T
from typing import Union, List
from magicdb import db, ASCENDING, DESCENDING, DocumentSnapshot
from magicdb.Queries.Q import Q
from magicdb.utils.Serverless.span import safe_span
from magicdb.utils.async_helpers import magic_async

import redis as redis_lib
import time
import ujson


class QuerySpeed:
    def __init__(self, cls):
        from magicdb.Models.MagicModelSpeed import MagicModelSpeed

        self.cls: MagicModelSpeed = cls
        self.collection_path = self.cls.get_collection_name()
        self.firebase_query = self.create_query()
        self.query_inputs: List[str] = []

    @property
    def redis(self) -> T.Optional[redis_lib.Redis]:
        return self.cls.get_redis()

    @property
    def redis_ttl_secs(self) -> T.Optional[int]:
        return self.cls.get_redis_ttl_secs()

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

    def get_path_of_query(self):
        if getattr(self.firebase_query, "_path", None):
            return "/".join(self.firebase_query._path)
        if getattr(self.firebase_query, "_parent", None):
            return "/".join(self.firebase_query._parent._path)
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

    @magic_async
    def get(
        self,
        id=None,
        create=False,
        validate_db_data=True,
        skip_redis=False,
        skip_redis_get=False,
        skip_redis_set=False,
        **kwargs,
    ):
        if skip_redis:
            skip_redis_get = True
            skip_redis_set = True
        if id:
            self.firebase_query = self.firebase_query.document(id)

        d = None
        redis_miss = False

        _key = self.get_path_of_query()
        _doc = None

        if self.redis and not skip_redis_get:
            with safe_span(self.make_safe_span_label("get-redis")):
                raw = self.redis.get(_key)
                if not raw:
                    redis_miss = True
                    print(f"Redis miss for {self.get_path_of_query()}.")
                else:
                    d = ujson.loads(raw)
        if not d:
            with safe_span(self.make_safe_span_label("get")):
                doc = self.firebase_query.get(**kwargs)
            if type(doc) != DocumentSnapshot:
                return None
            d = doc.to_dict()
            _doc = doc
            _key = doc.reference.path

        if not d:
            return None if not create else self.cls(id=id)

        constructor = self.cls if validate_db_data else self.cls.construct

        model = constructor(
            from_db=True,
            _doc=_doc,
            **d,
            _key=_key,
        )

        if redis_miss and not skip_redis_set:
            if self.redis_ttl_secs:
                with safe_span(self.make_safe_span_label("setex-redis")):
                    self.redis.setex(
                        name=self.get_path_of_query(),
                        time=self.redis_ttl_secs,
                        value=model.json(),
                    )
            else:
                with safe_span(self.make_safe_span_label("set-redis")):
                    self.redis.set(name=self.get_path_of_query(), value=model.json())

        return model

    @magic_async
    def get(
        self,
        id=None,
        create=False,
        validate_db_data=True,
        skip_redis=False,
        skip_redis_get=False,
        skip_redis_set=False,
        **kwargs,
    ):
        if skip_redis:
            skip_redis_get = True
            skip_redis_set = True
        if id:
            self.firebase_query = self.firebase_query.document(id)

        d = None
        redis_miss = False

        _key = self.get_path_of_query()
        _doc = None

        if self.redis and not skip_redis_get:
            with safe_span(self.make_safe_span_label("get-redis")):
                raw = self.redis.get(_key)
                if not raw:
                    redis_miss = True
                    print(f"Redis miss for {self.get_path_of_query()}.")
                else:
                    d = ujson.loads(raw)
        if not d:
            with safe_span(self.make_safe_span_label("get")):
                doc = self.firebase_query.get(**kwargs)
            if type(doc) != DocumentSnapshot:
                return None
            d = doc.to_dict()
            _doc = doc
            _key = doc.reference.path

        if not d:
            return None if not create else self.cls(id=id)

        constructor = self.cls if validate_db_data else self.cls.construct

        model = constructor(
            from_db=True,
            _doc=_doc,
            **d,
            _key=_key,
        )

        if redis_miss and not skip_redis_set:
            if self.redis_ttl_secs:
                with safe_span(self.make_safe_span_label("setex-redis")):
                    self.redis.setex(
                        name=self.get_path_of_query(),
                        time=self.redis_ttl_secs,
                        value=model.json(),
                    )
            else:
                with safe_span(self.make_safe_span_label("set-redis")):
                    self.redis.set(name=self.get_path_of_query(), value=model.json())

        return model

    @magic_async
    def get_all(
        self,
        ids,
        validate_db_data=True,
        skip_redis=False,
        skip_redis_get=False,
        skip_redis_set=False,
        **kwargs,
    ):
        if skip_redis:
            skip_redis_get = True
            skip_redis_set = True

        doc_refs = [db.conn.collection(self.collection_path).document(id) for id in ids]
        _keys = [doc_ref._path for doc_ref in doc_refs]

        docs = None
        redis_miss = False
        d_arr = None
        if self.redis and not skip_redis_get:
            with safe_span(self.make_safe_span_label("get_all-redis")):
                raw_arr = self.redis.mget(_keys)
                if None in raw_arr:
                    redis_miss = True
                    print(f"Redis miss for {self.get_path_of_query()}.")
                else:
                    d_arr = [ujson.loads(raw) for raw in raw_arr]
        if not d_arr:
            with safe_span(self.make_safe_span_label("get_all")):
                docs = list(db.conn.get_all(doc_refs, **kwargs))

        constructor = self.cls if validate_db_data else self.cls.construct

        models = []
        if d_arr:
            for key, d in zip(_keys, d_arr):
                models.append(constructor(from_db=True, _key=key, **d))
        else:
            for doc in docs:
                models.append(
                    constructor(
                        from_db=True, _key=doc.reference.path, _doc=doc, **doc.to_dict()
                    )
                )

        """
        models = [
            constructor(
                from_db=True,
                _doc=doc,
                **doc.to_dict(),
                _key=doc.reference.path,
            )
            for doc in docs
        ]
        """
        sorted_models = self.sort_models_by_id_order(models, ids)
        if redis_miss and not skip_redis_set:
            model_d = {model.key: model.json() for model in sorted_models}
            if self.redis_ttl_secs:
                with safe_span(
                    self.make_safe_span_label(f"msetex-redis-{len(model_d)}")
                ):
                    self.redis.setex(
                        name=self.get_path_of_query(),
                        time=self.redis_ttl_secs,
                        value=model.json(),
                    )
            else:
                with safe_span(self.make_safe_span_label("set-redis")):
                    self.redis.set(name=self.get_path_of_query(), value=model.json())

            self.redis.mset(model_d)

    @staticmethod
    def sort_models_by_id_order(models, ids):
        """Maintain order of return array"""
        sorted_models = [None] * len(ids)
        sort_key = {id: index for index, id in enumerate(ids)}
        for model in models:
            sorted_models[sort_key[model.id]] = model
        return sorted_models

    """Subcollections"""

    def collections(self):
        return self.firebase_query.collections()

    def collections_names(self):
        return [coll.id for coll in self.firebase_query.collections()]
