import time
import typing
from datetime import datetime
import pprint
from magicdb.Models import MagicModel, DateModel
import magicdb
import firebase_admin

from firebase_admin import firestore, credentials

# creds = credentials.Certificate("/Users/jeremyberman/Downloads/my-service-account.json")

# firebase_admin.initialize_app(creds)

# db = firestore.client()

import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "/Users/jeremyberman/Downloads/my-service-account.json"


class TestModel(MagicModel):
    # ref = db.collection("new_artists_9_16").document("1")
    name = "frankR"
    old_beatgig_data: typing.Dict = None
    spotify_api_data: typing.Dict = None

    class Meta:
        collection_name = "new_artists_9_16"
        # magic_fields_to_exclude = {"ref"}


class Change(MagicModel):
    name: str
    created_at: datetime

    class Meta:
        collection_name = "changes"


"""
# test_model = TestModel(id="1")
# test_model2 = TestModel(id="2", parent=test_model)
# print("22222", test_model2)
# print(test_model.collection_name)

print("ddd", test_model.dict())
print(test_model.json())
# print("ssss", test_model.schema())
print(test_model.ref.path)
# print("ssss", test_model2.schema())
print("jjjj", test_model.schema_json())
"""
# pprint.pprint(test_model.ref.__dict__)

# ref = db.collection("new_artists_9_16").document("1")
# print(type(ref) == magicdb.DocumentReference)
# print("ref", ref)

# models = TestModel.collection.limit(10).stream(validate_db_data=False)
# print(models)
# print(str(models[0]))

# m = TestModel.collection.get_all(ids=["123456", "1"])
# print("m", m)


def test_harber():
    harber_test = TestModel.collection.get(id="123456", validate_db_data=False)
    print("hhh", harber_test)
    print(type(harber_test))
    changes = (
        Change.collection.parent(harber_test)
        .order_by("created_at", "desc")
        .limit(2)
        .stream()
    )

    print("changes", changes)
    print(list(changes))

    print(harber_test.get_subcollections()[0].__dict__)

    start = time.time()
    new_test: TestModel = TestModel(**harber_test.dict())
    print("took", time.time() - start)
    print(new_test)

    q = Change.collection.parent(harber_test).order_by("created_at", "desc").limit(2)

    res = Change.stream_queries([q])
    print("RESSSS", res)


# test_harber()


class Teacher(MagicModel):
    name: str
    scuba: str = "snacks"
    hurr: str = None

    class Meta:
        collection_name = "teachers_testing"


def test_teacher():
    t = Teacher(name="sally")
    # t.save()
    print(t.__dict__)
    t.save()

    t.name = "henty"
    print("ttt", t)
    t.update()
    print("tttt", t)
    t.scuba = "rob"
    t.update()
    t.hurr = "['hi']"
    print("hu", t)
    t.update()
    t.save()

    h = Teacher(name="h")
    h.set_id("23")
    h.save()
    t.set_parent(h)
    print("tttttt", t)
    t.print_all()
    t.set_id("777")
    t.update(create=True)
    t.hurr = "uuuu"

    t.update()


class Dog(DateModel):
    name: str = "jon"
    has_bone: bool = False


def test_dog():
    dog1 = Dog()
    print(dog1)
    dog1.name = "tobu"
    print(dog1)


# test_dog()
