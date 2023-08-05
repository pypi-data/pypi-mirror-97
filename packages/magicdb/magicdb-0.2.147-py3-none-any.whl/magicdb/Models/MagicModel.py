from __future__ import annotations
import threading
from copy import deepcopy
import json
from typing import List, Dict, Any
import os
import concurrent.futures
from glom import glom
from datetime import datetime
import copy
import time
import pprint


import magicdb
from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass

from magicdb.Models import model_helpers
from magicdb.Queries import Query
from magicdb.utils.Serverless.span import safe_span

from magicdb.utils.updating_objects import make_update_obj

from magicdb.utils.async_helpers import threadpool_asyncio, threadpool, magic_async


from slugify import slugify as base_slugify

slugify_kwargs = {"separator": "", "replacements": [["&", "and"]]}

MAGIC_FIELDS = ["id", "key", "ref", "parent", "kwargs_from_db", "doc"]

# ref will break this cause it is not jsonable
MAGIC_FIELDS_TO_EXCLUDE = set(MAGIC_FIELDS) - {"id"}

FIELDS_TO_EXCLUDE_FOR_DB = set(MAGIC_FIELDS)


class DatabaseError(Exception):
    def __init__(self, key):
        self.message = (
            f"There is no document with key {key} to update. Add update.(create=True) to save the document"
            f" if it does not exist. Otherwise, you can save the document: save()."
        )


class QueryMeta(type):
    """https://stackoverflow.com/questions/128573/using-property-on-classmethods"""

    @property
    def collection(cls) -> Query:
        return Query(cls)

    @property
    def collection_group(cls) -> Query:
        return Query(cls).collection_group()


class QueryAndBaseMetaClasses(ModelMetaclass, QueryMeta):
    pass


class MagicModel(BaseModel, metaclass=QueryAndBaseMetaClasses):
    """
    When this gets inited, if given an id or key, assign based on that.
    Otherwise, assign them based on what Firestore gives it
    """

    id: str = None
    key: str = None
    # ref: magicdb.DocumentReference = None
    # doc: magicdb.DocumentSnapshot = None
    ref: Any = None
    doc: Any = None
    parent: MagicModel = None
    kwargs_from_db: dict = None

    __call__ = ...  # to satisfy Query python linter

    def __init__(self, from_db: bool = False, **kwargs):
        """Feed in all magic fields as kwargs"""
        # TODO test how slow this deep copy is
        kwargs_from_db = {} if not from_db else deepcopy(kwargs)
        model_helpers.make_magic_fields_from_kwargs(
            kwargs=kwargs, collection_name=self.collection_name
        )
        super().__init__(**kwargs)
        self.kwargs_from_db = kwargs_from_db

    @classmethod
    def construct(cls, *args, from_db: bool = False, **kwargs):
        kwargs_from_db = {} if not from_db else deepcopy(kwargs)
        model_helpers.make_magic_fields_from_kwargs(
            kwargs=kwargs, collection_name=cls.get_collection_name()
        )
        new_obj = super().construct(*args, **kwargs)
        new_obj.kwargs_from_db = kwargs_from_db
        return new_obj

    """GETTING AND SETTING FIELDS"""

    def set_id(self, id: str):
        kwargs = {"id": id}
        model_helpers.make_magic_fields_from_id_parent_or_nothing(
            kwargs=kwargs, collection_name=self.collection_name
        )
        self.__dict__.update(kwargs)

    def set_key(self, key: str):
        kwargs = {"key": key}
        model_helpers.make_magic_fields_from_key(kwargs=kwargs)
        self.__dict__.update(kwargs)

    def set_ref(self, ref: magicdb.DocumentReference):
        kwargs = {"ref": ref}
        model_helpers.make_magic_fields_from_ref(kwargs=kwargs)
        self.__dict__.update(kwargs)

    def set_parent(self, parent: MagicModel):
        kwargs = {"parent": parent}
        model_helpers.make_magic_fields_from_id_parent_or_nothing(
            kwargs=kwargs, collection_name=self.collection_name
        )
        self.__dict__.update(kwargs)

    """OVERRIDING PYDANTIC"""

    @classmethod
    def get_fields_to_exclude(cls):
        magic_fields_to_exclude = getattr(
            cls.Meta, "magic_fields_to_exclude", MAGIC_FIELDS_TO_EXCLUDE
        )
        given_fields_to_exclude = getattr(cls.Meta, "exclude", set())
        return magic_fields_to_exclude | given_fields_to_exclude

    def dict(self, exclude_magic_fields=True, *args, **kwargs):
        to_exclude = set() if not exclude_magic_fields else self.get_fields_to_exclude()
        # join w other fields passed in
        kwargs["exclude"] = kwargs.get("exclude") or set() | to_exclude
        return super().dict(*args, **kwargs)

    @classmethod
    def schema(cls, *args, **kwargs):
        """Temporarily take out the excluded fields to get the schema, then put them back."""

        original_fields = cls.__fields__.copy()

        for magic_field in cls.get_fields_to_exclude():
            if magic_field in cls.__fields__:
                del cls.__fields__[magic_field]

        schema_d = super().schema(*args, **kwargs)

        # cannot set __fields__ directly so will remove all items then update the d w the original fields
        for key in list(cls.__fields__.keys()):
            del cls.__fields__[key]

        cls.__fields__.update(original_fields)
        return schema_d

    """META CLASS FUNCTIONS"""

    @property
    def collection_name(self) -> str:
        return self.get_collection_name()

    @classmethod
    def make_default_collection_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_collection_name(cls) -> str:
        return getattr(cls.Meta, "collection_name", cls.make_default_collection_name())

    """PRINTING AND RETURNING"""

    def __repr__(self, *args, **kwargs):
        return f"{self.__class__.__name__}({self.__repr_str__(', ')})"

    def __str__(self, *args, **kwargs):
        return f"{self.__repr_str__(' ')}"

    def __repr_str__(self, join_str=", ", fields_to_exclude: set = None):
        fields_to_exclude: set = (
            fields_to_exclude
            if fields_to_exclude is not None
            else self.get_fields_to_exclude()
        )
        key_values: List[str] = []
        for field in self.__dict__:
            if field not in fields_to_exclude:
                key_values.append(f"{repr(field)}={repr(getattr(self, field, None))}")
        return join_str.join(key_values)

    def print_all(self):
        result: str = self.__repr_str__(fields_to_exclude=set())
        print("PRINT_ALL", result)
        return result

    """COMPARISONS"""

    def equal(self, model: BaseModel, path_to_compare=None):
        """The difference between objects will be firestore adds nanoseconds to the object. So parse those out"""
        replace_text = "+00:00"
        self_json = self.json().replace(replace_text, "")
        other_json = model.json().replace(replace_text, "")
        if path_to_compare:
            self_json = json.dumps(
                glom(json.loads(self_json), ".".join(path_to_compare))
            )
            other_json = json.dumps(
                glom(json.loads(other_json), ".".join(path_to_compare))
            )
        return self_json == other_json

    def been_updated(self, path_to_compare=None):
        from_db = self.__class__.get_with_error(self.id)
        return not self.equal(from_db, path_to_compare=path_to_compare)

    class Meta:
        """Init the meta class so you can use it and know it is there"""

        """Looks like having Meta in the TestModel actually overrites this one, not inherits it"""
        ...

    class Serverless:
        """Fills this with the latest context if it exists"""

        context = None

    class Config:
        anystr_strip_whitespace: bool = True

        arbitrary_types_allowed: bool = True

        @staticmethod
        def schema_extra(schema: Dict[str, Any], model: MagicModel) -> None:
            keys = list(schema.get("properties", {}).keys())
            to_exclude = model.get_fields_to_exclude()
            for key in keys:
                if key in to_exclude:
                    schema.get("properties", {}).pop(key)

        json_encoders = {magicdb.DocumentReference: lambda doc_ref: doc_ref.path}

    """ADDING TO FIRESTORE"""

    @staticmethod
    def remove_magic_fields(d):
        for magic_field in MAGIC_FIELDS:
            if magic_field in d:
                del d[magic_field]
        return d

    def save(self, batch=None, transaction=None, merge=False, ignore_fields=False):
        """Will create a new obj_to_save and save it so that all of the validation happens properly on a new obj."""
        batch_or_transaction = batch or transaction
        obj_to_save = (
            self
            if ignore_fields
            else self.__class__(**self.dict(exclude_magic_fields=False))
        )
        new_d = obj_to_save.dict()
        self.remove_magic_fields(new_d)

        with safe_span(f"save-{self.key}", use=(batch_or_transaction is None)):
            obj_to_save.ref.set(
                new_d, merge=merge
            ) if not batch_or_transaction else batch_or_transaction.set(
                obj_to_save.ref, new_d, merge=merge
            )
        if not merge:
            obj_to_save.kwargs_from_db = copy.deepcopy(new_d)

        # update self just in case
        self.__dict__.update(obj_to_save.__dict__)
        return obj_to_save

    def update(
        self,
        batch=None,
        transaction=None,
        create=False,
        ignore_fields=False,
        print_update_d=False,
        only_print_update_d=False,
    ):
        batch_or_transaction = batch or transaction
        # TODO this takes a long time... find out why and fix! Do you need to make new class?
        obj_to_update = (
            self
            if ignore_fields
            else self.__class__(**self.dict(exclude_magic_fields=False))
        )
        new_d = obj_to_update.dict()
        kwargs_d = self.kwargs_from_db

        self.remove_magic_fields(new_d)
        self.remove_magic_fields(kwargs_d)

        self.get_fields_to_exclude()
        update_d = (
            new_d if not kwargs_d else make_update_obj(original=kwargs_d, new=new_d)
        )
        if print_update_d or only_print_update_d:
            pprint.pprint({f"update_d_for_{self.id}": update_d})
        if only_print_update_d:
            return
        try:
            if update_d != {}:
                with safe_span(
                    f"update-{self.key}", use=(batch_or_transaction is None)
                ):
                    obj_to_update.ref.update(
                        update_d
                    ) if not batch_or_transaction else batch_or_transaction.update(
                        obj_to_update.ref, update_d
                    )
            else:
                print(f"update_d was empty so did not update for {self.id}.")
            self.__dict__.update(obj_to_update.__dict__)
            return obj_to_update
        except Exception as e:
            if hasattr(e, "message") and "no document to update" in e.message.lower():
                if create:
                    return obj_to_update.save(batch=batch, transaction=transaction)
                else:
                    db_error = DatabaseError(obj_to_update.key)
                    raise DatabaseError(db_error.message)
            raise e

    def delete(self, batch=None, transaction=None):
        batch_or_transaction = batch or transaction
        with safe_span(f"delete-{self.key}", use=(batch_or_transaction is None)):
            return (
                self.ref.delete()
                if not batch_or_transaction
                else batch_or_transaction.delete(self.ref)
            )

    """Save history to DB"""

    def save_history(self, sync: bool = True, user_id: str = None, **kwargs):
        """Saves current object to a changes sub collection"""
        history_key = f"{self.key}/history/{str(int(time.time()))}"

        class History(self.__class__):
            changed_at: datetime = Field(default_factory=datetime.utcnow)
            changed_by: str = user_id

        history_obj = History(**self.dict(), key=history_key)
        return history_obj.save(**kwargs) if sync else history_obj.save_async(**kwargs)

    def save_deleted(self, sync: bool = True, user_id: str = None, **kwargs):
        deleted_key = f"deleted_{self.collection_name}/{self.id}"

        class Deleted(self.__class__):
            deleted_at: datetime = Field(default_factory=datetime.utcnow)
            deleted_by: str = user_id

        deleted_obj = Deleted(**self.dict(), key=deleted_key)
        return deleted_obj.save(**kwargs) if sync else deleted_obj.save_async(**kwargs)

    """Writing to DB async"""

    def save_async(self, *args, **kwargs) -> threading.Thread:
        t = threading.Thread(target=self.save, args=(*args,), kwargs={**kwargs})
        t.start()
        return t

    def update_async(self, *args, **kwargs) -> threading.Thread:
        t = threading.Thread(target=self.update, args=(*args,), kwargs={**kwargs})
        t.start()
        return t

    def delete_async(self, *args, **kwargs) -> threading.Thread:
        t = threading.Thread(target=self.delete, args=(*args,), kwargs={**kwargs})
        t.start()
        return t

    """QUERYING AND COLLECTIONS"""

    def exists(self):
        return self.__class__.collection.get(self.id) is not None

    def get_subcollections(self):
        return list(self.__class__.collection.document(self.id).collections())

    @classmethod
    def get_ref(cls, id) -> magicdb.DocumentReference:
        temp_cls = cls.construct(id=id)
        return temp_cls.ref

    @classmethod
    def get_default_exception(cls):
        return getattr(cls.Meta, "default_exception", Exception)

    @classmethod
    @magic_async
    def get_with_error(cls, id, error=None, **kwargs):
        if not error:
            error = cls.get_default_exception()
        val = cls.collection.get(id, **kwargs)
        if not val:
            raise error(f"{cls.__name__} with id {id} does not exist.")
        return val

    @classmethod
    @threadpool_asyncio
    def get_with_error_async(cls, id, error=None, **kwargs):
        if not error:
            error = cls.get_default_exception()
        val = cls.collection.get(id, **kwargs)
        if not val:
            raise error(f"{cls.__name__} with id {id} does not exist.")
        return val

    @classmethod
    @threadpool_asyncio
    def get_async(cls, id, **kwargs):
        return cls.collection.get(id, **kwargs)

    @classmethod
    @threadpool
    def get_with_error_future(cls, id, error=None, **kwargs):
        if not error:
            error = cls.get_default_exception()
        val = cls.collection.get(id, **kwargs)
        if not val:
            raise error(f"{cls.__name__} with id {id} does not exist.")
        return val

    """GETTING SUBCLASSES"""

    @classmethod
    def get_subclasses(cls):
        all_subs = []
        for sub in cls.__subclasses__():
            all_subs.append(sub)
            all_subs += sub.get_subclasses()
        return list(set(all_subs))

    @staticmethod
    def get_all_subclasses_of_model():
        all_subs = []
        for sub in list(MagicModel.__subclasses__()):
            all_subs.append(sub)
            all_subs += sub.get_subclasses()
        return list(set(all_subs))

    @staticmethod
    def stream_queries(queries: List[magicdb.Query]):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # set this to 10 because lambda only has 2 cores so would only have 6 threads for max_workers
            # executor._max_workers = max(executor._max_workers, 20)
            futures = [
                executor.submit(
                    query.stream,
                )
                for query in queries
            ]
            return [f.result() for f in futures]

    """SLUG STUFF"""

    @classmethod
    def slugify(cls, slug):
        return base_slugify(slug, **slugify_kwargs)

    @classmethod
    def create_slug_static(cls, value_to_slugify: str):
        slug_base = cls.slugify(value_to_slugify.lower().replace(" ", ""))
        number = 1
        slug = slug_base
        while cls.get_by_slug(slug):
            slug = cls.slugify(f"{slug_base}{number}")
            number += 1
        return slug

    def create_slug(self, field_to_slugify: str = "name"):
        base_val = getattr(self, field_to_slugify, "")
        slug_base = self.__class__.slugify(base_val.lower().replace(" ", ""))
        number = 1
        slug = slug_base
        while not self.unique_slug(slug):
            slug = self.__class__.slugify(f"{slug_base}{number}")
            number += 1
        self.slug = slug
        return self.slug

    def unique_slug(self, slug):
        models = self.__class__.collection.where("slug", "==", slug).stream()
        for model in models:
            if model.id != self.id:
                return False
        return True

    @classmethod
    def get_by_slug(cls, slug):
        models = cls.collection.where("slug", "==", slug).stream()
        return None if not models else models[0]

    @classmethod
    def get_by_slug_with_error(cls, slug, error=None):
        if not error:
            error = cls.get_default_exception()
        models = cls.collection.where("slug", "==", slug).stream()
        if not models:
            raise error(f"{cls.__name__} with slug {slug} does not exist.")
        return models[0]

    @classmethod
    @magic_async
    def get_by_field(cls, field_name: str, value):
        models = cls.collection.where(
            magicdb.db.conn.field_path(field_name), "==", value
        ).stream()
        return None if not models else models[0]

    @classmethod
    @threadpool_asyncio
    def get_by_field_async(cls, field_name: str, value):
        return cls.get_by_field(field_name=field_name, value=value)

    @classmethod
    def get_by_field_with_error(cls, field_name: str, value, error=None):
        if not error:
            error = cls.get_default_exception()
        model = cls.get_by_field(field_name=field_name, value=value)
        if not model:
            raise error(f"{cls.__name__} with {field_name} {value} does not exist.")
        return model

    @classmethod
    @threadpool_asyncio
    def get_by_field_with_error_async(cls, field_name: str, value, error=None):
        return cls.get_by_field_with_error(
            field_name=field_name, value=value, error=error
        )


MagicModel.update_forward_refs()
