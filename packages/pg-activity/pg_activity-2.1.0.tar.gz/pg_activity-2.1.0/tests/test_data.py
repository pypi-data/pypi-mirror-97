import pytest

from pgactivity.data import Data, pg_get_version


@pytest.fixture
def data(postgresql):
    return Data.pg_connect(
        1,
        host=postgresql.info.host,
        port=postgresql.info.port,
        database=postgresql.info.dbname,
        user=postgresql.info.user,
    )


def test_pg_get_version(data):
    pg_get_version(data.pg_conn)


def test_pg_get_db_info(data):
    dbinfo = data.pg_get_db_info(None)
    assert set(dbinfo) == {
        "timestamp",
        "no_xact",
        "total_size",
        "max_length",
        "tps",
        "size_ev",
    }
