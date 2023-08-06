import sys
from os import environ

import pg8000.native

import pytest


@pytest.fixture(scope="class")
def db_kwargs():
    db_connect = {
        'user': 'postgres',
        'password': 'pw'
    }

    for kw, var, f in [
                ('host', 'PGHOST', str),
                ('password', 'PGPASSWORD', str),
                ('port', 'PGPORT', int)
            ]:
        try:
            db_connect[kw] = f(environ[var])
        except KeyError:
            pass

    return db_connect


@pytest.fixture
def con(request, db_kwargs):
    conn = pg8000.native.Connection(**db_kwargs)

    def fin():
        conn.run("rollback")
        try:
            conn.close()
        except pg8000.native.InterfaceError:
            pass

    request.addfinalizer(fin)
    return conn


@pytest.fixture
def is_java():
    return 'java' in sys.platform.lower()
