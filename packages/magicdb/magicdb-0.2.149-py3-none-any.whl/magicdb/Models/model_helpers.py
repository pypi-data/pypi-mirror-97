from magicdb import db

"""MAGIC MODEL MAGIC FIELDS HELPERS"""


def make_magic_fields_from_kwargs(kwargs: dict, collection_name: str) -> None:
    """Will make magic_fields either from key, ref, or id (included no id given or parent given).
    Whichever one exists, in that order."""
    if kwargs.get("key", None):
        make_magic_fields_from_key(kwargs)
    elif kwargs.get("ref", None):
        make_magic_fields_from_ref(kwargs)
    else:
        make_magic_fields_from_id_parent_or_nothing(kwargs, collection_name)


def make_magic_fields_from_key(kwargs):
    kwargs["ref"] = db.conn.document(kwargs["key"])
    kwargs["id"] = id_from_ref(kwargs["ref"])


def make_magic_fields_from_ref(kwargs):
    kwargs["key"] = key_from_ref(kwargs["ref"])
    kwargs["id"] = id_from_ref(kwargs["ref"])


def make_magic_fields_from_id_parent_or_nothing(kwargs, collection_name):
    """Assigns db_fields fields using an id if given. Otherwise, makes an id... Also uses parent if necessary."""
    collection_ref = (
        db.conn.collection(collection_name)
        if not kwargs.get("parent")
        else kwargs.get("parent").ref.collection(collection_name)
    )
    kwargs["ref"] = (
        collection_ref.document()
        if not kwargs.get("id")
        else collection_ref.document(kwargs.get("id"))
    )
    make_magic_fields_from_ref(kwargs)


def id_from_ref(ref):
    return ref.path.split("/")[-1]


def key_from_ref(ref):
    return ref.path
