from pathlib import Path

import pytest

import atoti as tt
from atoti._plugins import MissingPluginError

PROJECT_PATH = Path(__file__).parent.parent.parent.parent
DATABASE_PATH = (
    PROJECT_PATH
    / "java"
    / "plugins"
    / "sql-source"
    / "src"
    / "test"
    / "resources"
    / "h2database"
)
DATABASE_URL = "h2:" + str(DATABASE_PATH.absolute())
H2_USERNAME = "root"
H2_PASSWORD = ""

SCHEMA = {
    "ID": tt.type.INT,
    "CITY": tt.type.STRING,
    "MY_VALUE": tt.type.NULLABLE_DOUBLE,
}
CREDENTIALS = {"username": H2_USERNAME, "password": H2_PASSWORD}
SQL_QUERY = "SELECT * FROM MYTABLE;"


class ASqlTest:
    @classmethod
    def setup_class(cls):
        cls.session = tt.create_session()

    @classmethod
    def teardown_class(cls):
        cls.session.close()

    @pytest.fixture(autouse=True)
    def clear_test_session(self):
        """Run the test then clear the session."""
        yield
        self.session._clear()  # pylint: disable=protected-access


@pytest.mark.sql
class TestLoadSql(ASqlTest):
    def test_load_sql_h2_database(self):
        store = self.session.create_store(SCHEMA, "test sql", keys=["ID"])
        assert len(store) == 0
        store.load_sql(DATABASE_URL, SQL_QUERY, **CREDENTIALS)
        assert len(store) == 5

    def test_read_sql_h2_database(self):
        store = self.session.read_sql(
            "jdbc:" + str(DATABASE_URL),
            SQL_QUERY,
            **CREDENTIALS,
            store_name="sql",
            keys=["ID"],
        )
        assert len(store) == 5
        assert store.columns == ["ID", "CITY", "MY_VALUE"]
        assert store._types == SCHEMA  # pylint: disable=protected-access


class TestMissingSqlPlugin(ASqlTest):
    """Test without loading the module."""

    def test_missing_plugin_load_sql(self):
        store = self.session.create_store(SCHEMA, "test sql", keys=["ID"])
        with pytest.raises(MissingPluginError):
            store.load_sql(DATABASE_URL, SQL_QUERY, **CREDENTIALS)

    def test_missing_plugin_create_sql(self):
        with pytest.raises(MissingPluginError):
            self.session.read_sql(
                DATABASE_URL,
                SQL_QUERY,
                store_name="sql",
                **CREDENTIALS,
            )
