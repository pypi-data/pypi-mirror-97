# simple_firebase_realtime_db

![PyPI - package version](https://img.shields.io/pypi/v/simple_firebase_realtime_db?logo=pypi&style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/simple_firebase_realtime_db?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/simple_firebase_realtime_db?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/simple_firebase_realtime_db?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/py_simple_firebase_realtime_db?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/py_simple_firebase_realtime_db?style=flat-square)

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/py_simple_firebase_realtime_db?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/py_simple_firebase_realtime_db?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/py_simple_firebase_realtime_db?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/py_simple_firebase_realtime_db?label=repo%20license&style=flat-square)

## Description

simplified usage of firebase realtime database

## Install

~~~~bash
pip install simple_firebase_realtime_db
# or
pip3 install simple_firebase_realtime_db
~~~~

## Usage

~~~~python
from simple_firebase_realtime_db import FirebaseRealtimeDB as DB
import time

DB.initialize(
    certificate_path='',
    database_url=''
)

path = 'desired/path'

print(
    'set',
    DB.set(
        {
            'test-key':'test-value'
        },
        path
    )
)

time.sleep(10)

import json
print(json.dumps(DB.get(path), indent=4))

time.sleep(10)

print('delete', DB.delete(path))
~~~~

## Dependencies

[firebase-admin](https://pypi.org/project/firebase-admin), [jsoncodable](https://pypi.org/project/jsoncodable), [noraise](https://pypi.org/project/noraise)