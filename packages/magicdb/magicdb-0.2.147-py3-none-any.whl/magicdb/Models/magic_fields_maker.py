import typing as T
import magicdb
from magicdb import db
from magicdb.Models import MagicModelSpeed


class FieldMaker:
    def __init__(
        self,
        *,
        _key: str = None,
        _ref: magicdb.DocumentReference = None,
        _collection_name: str,
        id: str = None,
        _parent: MagicModelSpeed = None,
        **kwargs,  # this is so that all fields can be passed and I only keep ones that matter
    ):
        self._key = _key
        self._ref = _ref
        self.collection_name = _collection_name
        self.id = id
        self._parent = _parent

        self.make_magic_fields_from_scratch()

    @classmethod
    def from_model(cls, magic_model: MagicModelSpeed):
        return cls(
            _key=magic_model._key,
            _ref=magic_model._ref,
            _collection_name=magic_model.get_collection_name(),
            id=magic_model.id,
            _parent=magic_model._parent,
        )

    def make_magic_fields_from_scratch(self):
        if self._key:
            self.from_key()
        elif self._ref:
            self.from_ref()
        else:
            self.from_id_parent_collection_name()

    def set_model_fields(
        self, magic_model: MagicModelSpeed, fields_to_exclude: T.Set[str] = None
    ):
        if not fields_to_exclude:
            fields_to_exclude = set()

        if "id" not in fields_to_exclude:
            magic_model._id = self.id
        if "key" not in fields_to_exclude:
            magic_model._key = self._key
        if "ref" not in fields_to_exclude:
            magic_model._ref = self._ref
        if "parent" not in fields_to_exclude:
            magic_model._parent = self._parent

    def from_ref(self):
        self.key_from_ref()
        self.id_from_ref()

    def from_key(self):
        self.ref_from_key()
        self.from_ref()

    def from_id_parent_collection_name(self):
        base_ref = db.conn if not self._parent else self._parent._ref
        coll_ref = base_ref.collection(self.collection_name)
        self._ref = coll_ref.document() if not self.id else coll_ref.document(self.id)
        self.from_ref()

    def id_from_key(self):
        self.id = self._key.split("/")[-1]

    def id_from_ref(self):
        self.id = self._ref.path.split("/")[-1]

    def ref_from_key(self):
        self._ref = db.conn.document(self._key)

    def key_from_ref(self):
        self._key = self._ref.path
