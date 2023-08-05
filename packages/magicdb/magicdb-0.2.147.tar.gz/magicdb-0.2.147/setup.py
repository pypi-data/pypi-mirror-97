# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magicdb',
 'magicdb.Fields',
 'magicdb.FirestoreWrappers',
 'magicdb.Models',
 'magicdb.Queries',
 'magicdb.Timing',
 'magicdb.database',
 'magicdb.utils',
 'magicdb.utils.Redis',
 'magicdb.utils.Serverless']

package_data = \
{'': ['*']}

install_requires = \
['firebase-admin>=4.4.0,<5.0.0',
 'glom>=20.8.0,<21.0.0',
 'grpcio>=1.34.0,<2.0.0',
 'phonenumbers>=8.12.19,<9.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-google-places>=1.4.2,<2.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'redis>=3.5.3,<4.0.0',
 'ujson>=3.0.0']

setup_kwargs = {
    'name': 'magicdb',
    'version': '0.2.147',
    'description': '',
    'long_description': '# MagicDB\nA fully typed Firestore ORM for python -- the easiest way to store data.\n\nMagicDB inherets from Pydantic, so you get all the power of Pydantic models with the functionality of Firestore: https://pydantic-docs.helpmanual.io/.\n\n## Instalation\n```\npip install magicdb\n```\n\n## Initialize the DB\nMagicDB is initialized via a Firestore service account json which you download from your Firebase console.\nOnce you have the json, you must tell MagicDB where it is, either by 1) setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the json path, or by 2) calling magicdb.connect with the path:\n\n```python\n# 1)\n# You can set the env variable from the terminal too: export GOOGLE_APPLICATION_CREDENTIALS="path/to/my-service-account.json"\nimport os\nos.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/my-service-account.json"\n\n# OR\n\n# 2)\nimport magicdb\nmagicdb.connect(from_file="path/to/my-service-account.json")\n```\n\n## Example\n```python\nfrom magicdb.Models import MagicModel\n\nclass Salesman(MagicModel):\n    name: str = None\n    company: str = None\n\ns = Salesman()\ns.name = \'Jim\'\ns.save()\n\n# Get Salesman\ns = Salesman.collection.get(s.id)\nprint(s.name) # Jim\n```\n\n## Fields\nUse any type [mypy](http://mypy-lang.org/) will accept!\n\n#### Fields Example\n```python\nfrom datetime import datetime\n\nclass Manager(MagicModel):\n\tname: str\n\tage: int\n\tcompany: str = \'Dunder Mifflin\'\n\tstartedWorkingAt: datetime = None\n\n# m = Manager(name=\'Michael Scott\', age=44)  # you must pass in the required fields on initializing the object.\nm.age = 45\nm.save()  # Success! New doc in collection "manager" as: { name: Michael Scott, age: 45, company: Dunder Mifflin }\n\nm = Manager(name=\'Dwight Schrute\') # Exception since age is required but not given\n```\n\nYou can also add other Objects as a field.\n\n### NestedModel Example\n```python\nclass Dog(MagicModel):\n\tage: int\n\towner: Manager\n\ndog = Dog()\ndog.age = 3\ndog.owner = Manager(name=\'Robert California\', age=59)\ndog.save()\nprint(dog)\n\n```\n\n\n## Collections\nThe collection name for a class defaults to the class\' name in lowercase. To set the collection name, use the `Meta` class.\n\n### Meta Example\n\n```python\nclass Student(MagicModel):\n\tname: str = None\n\tschool: str = \'UPenn\'\n\n\tclass Meta:\n\t\tcollection_name = \'students\'\n\n\ns = Student(name=\'Amy Gutman\')\ns.save()  # creates a new document in the "students" collection\nprint(s)  # name=\'Amy Gutman\' school=\'UPenn\'\n```\n\nYou can also inheret classes.\n\n### Inheritance Example\n```python\nclass ExchangeStudent(Student):\n\toriginalCountry: str\n\n\tclass Meta:\n\t\tcollection_name = \'exchangeStudents\'\n\ne = ExchangeStudent(originalCountry=\'UK\')\nprint(e.school)  # UPenn\ne.save()\nprint(e)  # name=None school=\'UPenn\' originalCountry=\'UK\'\n```\n\n## Queries\nYou can make queries with the same syntax you would using the Python firebase-admin SDK. But FireORM returns the objects.\n\n### Queries Example\n```python\n\ne = ExchangeStudent(originalCountry=\'UK\')\nprint(e.school)  # UPenn\ne.save()\nprint(e)  # name=None school=\'UPenn\' originalCountry=\'UK\'\n\nmanagers = Manager.collection.where(\'name\', \'==\', \'Michael Scott\').limit(1).stream()\nprint(managers) # [Manager(name=\'Michael Scott\', age=45, company=\'Dunder Mifflin\', startedWorkingAt=None)]\nprint(managers[0].id)\nmanager = Manager.collection.get(\'0mIWZ8FfgQzBanCllqsV\')\nprint(manager) # name=\'Michael Scott\' age=45 company=\'Dunder Mifflin\' startedWorkingAt=None\n```\n',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jerber/magicdb_new',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
