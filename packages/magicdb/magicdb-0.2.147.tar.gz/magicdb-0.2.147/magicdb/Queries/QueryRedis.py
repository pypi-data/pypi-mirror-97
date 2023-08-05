from __future__ import annotations
import typing as T

import redis

from .QuerySpeed import QuerySpeed

from magicdb.utils.Serverless.span import safe_span
from magicdb.utils.async_helpers import magic_async


class QueryRedis(QuerySpeed):
    ...

    def get_d_from_db(self, **kwargs) -> dict:
        # first try redis, then do firestore if miss
        key = self.get_path_of_query()

        with safe_span(self.make_safe_span_label("get-redis")):
            if d := self.r.get(key):
                print("Redis hit!")
                return d

        print("Redis miss!")
        # there was a cache miss
        model = super().get_d_from_db(**kwargs)
        if model:
            with safe_span(self.make_safe_span_label("set-redis")):
                self.r.set(key)

    def get(self, id=None, *args, **kwargs):
        # if cache miss
        if id:
            self.firebase_query = self.firebase_query.document(id)
        key = self.get_path_of_query()

        if d := self.r.get(key):
            ...

        model = super().get(*args, **kwargs)
        self.r.set(key, model.json())
        return model

    @property
    def r(self) -> T.Optional[redis.Redis]:
        return self.cls.get_redis()

    @property
    def r_ttl_secs(self) -> T.Optional[int]:
        return self.cls.get_redis_ttl_secs()
