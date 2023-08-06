import socket
import struct

import pg8000

import pytest


def testUnixSocketMissing():
    conn_params = {
        'unix_sock': "/file-does-not-exist",
        'user': "doesn't-matter"
    }

    with pytest.raises(pg8000.dbapi.InterfaceError):
        pg8000.dbapi.connect(**conn_params)


def test_internet_socket_connection_refused():
    conn_params = {
        'port': 0,
        'user': "doesn't-matter"
    }

    with pytest.raises(
            pg8000.dbapi.InterfaceError,
            match="Can't create a connection to host localhost and port 0 "
            "\\(timeout is None and source_address is None\\)."):
        pg8000.dbapi.connect(**conn_params)


def testDatabaseMissing(db_kwargs):
    db_kwargs["database"] = "missing-db"
    with pytest.raises(pg8000.dbapi.DatabaseError):
        pg8000.dbapi.connect(**db_kwargs)


def test_notify(con):
    cursor = con.cursor()
    cursor.execute("select pg_backend_pid()")
    backend_pid = cursor.fetchall()[0][0]
    assert list(con.notifications) == []
    cursor.execute("LISTEN test")
    cursor.execute("NOTIFY test")
    con.commit()

    cursor.execute("VALUES (1, 2), (3, 4), (5, 6)")
    assert len(con.notifications) == 1
    assert con.notifications[0] == (backend_pid, "test", '')


def test_notify_with_payload(con):
    cursor = con.cursor()
    cursor.execute("select pg_backend_pid()")
    backend_pid = cursor.fetchall()[0][0]
    assert list(con.notifications) == []
    cursor.execute("LISTEN test")
    cursor.execute("NOTIFY test, 'Parnham'")
    con.commit()

    cursor.execute("VALUES (1, 2), (3, 4), (5, 6)")
    assert len(con.notifications) == 1
    assert con.notifications[0] == (backend_pid, "test", 'Parnham')


def testUnicodeDatabaseName(db_kwargs):
    db_kwargs["database"] = "pg8000_sn\uFF6Fw"

    # Should only raise an exception saying db doesn't exist
    with pytest.raises(pg8000.dbapi.DatabaseError, match='3D000'):
        pg8000.dbapi.connect(**db_kwargs)


def testBytesDatabaseName(db_kwargs):
    """ Should only raise an exception saying db doesn't exist """

    db_kwargs["database"] = bytes("pg8000_sn\uFF6Fw", 'utf8')
    with pytest.raises(pg8000.dbapi.DatabaseError, match='3D000'):
        pg8000.dbapi.connect(**db_kwargs)


def testBytesPassword(con, db_kwargs):
    # Create user
    username = 'boltzmann'
    password = 'cha\uFF6Fs'
    cur = con.cursor()
    cur.execute(
        "create user " + username + " with password '" + password + "';")
    con.commit()

    db_kwargs['user'] = username
    db_kwargs['password'] = password.encode('utf8')
    db_kwargs['database'] = 'pg8000_md5'
    with pytest.raises(pg8000.dbapi.DatabaseError, match='3D000'):
        pg8000.dbapi.connect(**db_kwargs)

    cur.execute("drop role " + username)
    con.commit()


def test_broken_pipe(con, db_kwargs):
    with pg8000.dbapi.connect(**db_kwargs) as db1:
        cur1 = db1.cursor()
        cur2 = con.cursor()
        cur1.execute("select pg_backend_pid()")
        pid1 = cur1.fetchone()[0]

        cur2.execute("select pg_terminate_backend(%s)", (pid1,))
        try:
            cur1.execute("select 1")
        except Exception as e:
            assert isinstance(e, (socket.error, struct.error))


def testApplicatioName(db_kwargs):
    app_name = 'my test application name'
    db_kwargs['application_name'] = app_name
    with pg8000.dbapi.connect(**db_kwargs) as db:
        cur = db.cursor()
        cur.execute(
            'select application_name from pg_stat_activity '
            ' where pid = pg_backend_pid()')

        application_name = cur.fetchone()[0]
        assert application_name == app_name


def test_application_name_integer(db_kwargs):
    db_kwargs['application_name'] = 1
    with pytest.raises(
            pg8000.dbapi.InterfaceError,
            match="The parameter application_name can't be of type "
            "<class 'int'>."):
        pg8000.dbapi.connect(**db_kwargs)


def test_application_name_bytearray(db_kwargs):
    db_kwargs['application_name'] = bytearray(b'Philby')
    pg8000.dbapi.connect(**db_kwargs)
