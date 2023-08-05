from pydantic import BaseModel, Field, PrivateAttr
import magicdb
from magicdb import db
from magicdb.Models import MagicModelSpeed


class MagicFieldsCreator(BaseModel):
    id: str = None
    _key: str = PrivateAttr(None)
    _ref: magicdb.DocumentReference = PrivateAttr(None)
    _doc: magicdb.DocumentSnapshot = PrivateAttr(None)
    _parent: MagicModelSpeed = PrivateAttr(None)

    @staticmethod
    def make_magic_fields(magic_model: MagicModelSpeed, data: dict):
        MagicFieldsCreator()._make_magic_fields(magic_model, data)

    def _make_magic_fields(self, magic_model: MagicModelSpeed, data: dict):
        for field in self.__annotations__.keys():
            setattr(self, field, data.get(field, None))
        if self._key:
            self.fields_from_key()
        if self._ref:
            self.fields_from_ref()
        else:
            self.fields_from_id_parent_nothing(magic_model.collection_name)

        magic_model.id = self.id
        magic_model._key = self._key
        magic_model._ref = self._ref
        magic_model._doc = self._doc
        magic_model._parent = self._parent

    def fields_from_key(self):
        self._ref = db.conn.document(self._key)
        self.id = self.id_from_ref(self._ref)

    def fields_from_ref(self):
        self._key = self.key_from_ref(self._ref)
        self.id = self.id_from_ref(self._ref)

    def fields_from_id_parent_nothing(self, collection_name: str):
        base_ref = db.conn if not self._parent else self._parent._ref
        coll_ref = base_ref.collection(collection_name)
        self._ref = coll_ref.document() if not self.id else coll_ref.document(self.id)
        self.fields_from_ref()

    @staticmethod
    def id_from_ref(ref):
        return ref.path.split("/")[-1]

    @staticmethod
    def key_from_ref(ref):
        return ref.path

    """SETTING AND GETTING"""

    @staticmethod
    def set_id(magic_model: MagicModelSpeed, id: str):
        MagicFieldsCreator()._make_magic_fields(magic_model, {"id": id})

    @staticmethod
    def set_key(magic_model: MagicModelSpeed, key: str):
        MagicFieldsCreator()._make_magic_fields(magic_model, {"_key": key})

    @staticmethod
    def set_ref(magic_model: MagicModelSpeed, ref: magicdb.DocumentReference):
        MagicFieldsCreator()._make_magic_fields(magic_model, {"_ref": ref})

    @staticmethod
    def set_parent(magic_model: MagicModelSpeed, parent: MagicModelSpeed):
        MagicFieldsCreator()._make_magic_fields(magic_model, {"_parent": parent})
