from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Collection, Mapping, Optional, Union

from atoti._docs_utils import STORE_CREATION_KWARGS, STORE_SHARED_KWARGS, doc
from atoti._sources import DataSource
from atoti.sampling import FULL
from atoti.store import _create_store

from .drivers import _infer_driver

if TYPE_CHECKING:
    from atoti._java_api import JavaApi
    from atoti.sampling import SamplingMode
    from atoti.session import Session
    from atoti.simulation import ScenarioName, Simulation
    from atoti.store import Store
    from atoti.type import DataType

JDBC_PREFIX = "jdbc:"

SQL_KWARGS = {
    "url": """url: The URL of the database.
            For instance:

                * ``mysql:localhost:7777/example``
                * ``h2:/home/user/database/file/path``""",
    "query": """query: A SQL query which result is used to build a store.""",
    "username": """username: The username used to connect to the database.""",
    "password": """password: The password used to connect to the database.""",
    "driver": """driver: The JDBC driver used to load the data.
            If ``None``, the driver is inferred from the URL.
            Drivers can be found in the :mod:`atoti_sql.drivers` module.""",
}


def create_sql_params(
    url: str,
    query: str,
    username: str,
    password: str,
    driver_class: str,
) -> Mapping[str, Any]:
    """Create the SQL spefic parameters."""
    return {
        "url": url,
        "query": query,
        "username": username,
        "password": password,
        "driverClass": driver_class,
    }


class SqlDataSource(DataSource):
    """SQL data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "JDBC")

    def load_sql_into_store(
        self,
        store: Union[Store, Simulation],
        scenario_name: Optional[ScenarioName],
        in_all_scenarios: bool,
        truncate: bool,
        url: str,
        query: str,
        username: str,
        password: str,
        driver: str,
    ):
        """Load the data from SQL database into the store."""
        source_params = create_sql_params(url, query, username, password, driver)
        self.load_data_into_store(
            store.name,
            scenario_name,
            in_all_scenarios,
            False,
            truncate,
            source_params,
        )

    def read_sql_into_store(
        self,
        store_name: str,
        keys: Optional[Collection[str]],
        partitioning: Optional[str],
        types: Optional[Mapping[str, DataType]],
        sampling: SamplingMode,
        url: str,
        query: str,
        username: str,
        password: str,
        driver: str,
        hierarchized_columns: Optional[Collection[str]],
    ):
        """Create a store from the SQL database."""
        source_params = create_sql_params(url, query, username, password, driver)
        self.create_store_from_source(
            store_name,
            keys,
            partitioning,
            types,
            sampling,
            True,
            False,
            source_params,
            hierarchized_columns,
        )


def clear_url(url: Union[str, Path]) -> str:
    if isinstance(url, Path):
        url = str(url.absolute())
    if not url.startswith(JDBC_PREFIX):
        url = JDBC_PREFIX + url
    return url


@doc(**{**STORE_SHARED_KWARGS, **STORE_CREATION_KWARGS, **SQL_KWARGS})
def read_sql(
    self: Session,
    url: Union[Path, str],
    query: str,
    *,
    username: str,
    password: str,
    driver: Optional[str] = None,
    store_name: str,
    keys: Optional[Collection[str]] = None,
    partitioning: Optional[str] = None,
    types: Optional[Mapping[str, DataType]] = None,
    hierarchized_columns: Optional[Collection[str]] = None,
) -> Store:
    """Create a store from the result of the passed SQL query.

    Note:
        This method requires the :mod:`atoti-sql <atoti_sql>` plugin.

    Args:
        {url}
        {query}
        {username}
        {password}
        {driver}
        {store_name}
        {keys}
        {partitioning}
        types: Types for some or all columns of the store.
            Types for non specified columns will be inferred from the SQL types.
        {hierarchized_columns}

    Example:
        .. doctest:: read_sql

            >>> store = session.read_sql(
            ...     f"h2:{{RESOURCES}}/h2-database",
            ...     "SELECT * FROM MYTABLE;",
            ...     username="root",
            ...     password="pass",
            ...     store_name="Cities",
            ...     keys=["ID"],
            ... )

        .. doctest:: read_sql
            :hide:

            Remove the edited H2 database from Git's working tree.
            >>> session.close()
            >>> import os
            >>> os.system(f"git checkout -- {{RESOURCES}}/h2-database.mv.db")
            0

    """
    url = clear_url(url)
    if driver is None:
        driver = _infer_driver(url)
    SqlDataSource(
        self._java_api  # pylint: disable=protected-access
    ).read_sql_into_store(
        store_name,
        keys,
        partitioning,
        types,
        FULL,  # We don't support any other sampling at the moment
        url,
        query,
        username,
        password,
        driver,
        hierarchized_columns,
    )
    return _create_store(self._java_api, store_name)  # pylint: disable=protected-access


@doc(**{**STORE_SHARED_KWARGS, **SQL_KWARGS})
def load_sql(
    self: Store,
    url: Union[Path, str],
    query: str,
    *,
    username: str,
    password: str,
    driver: Optional[str] = None,
    in_all_scenarios: bool = False,
    truncate: bool = False,
):
    """Load the result of the passed SQL query into the store.

    Note:
        This method requires the :mod:`atoti-sql <atoti_sql>` plugin.

    Args:
        {url}
        {query}
        {username}
        {password}
        {driver}
        {in_all_scenarios}
        {truncate}
    """
    url = clear_url(url)
    if driver is None:
        driver = _infer_driver(url)
    SqlDataSource(
        self._java_api  # pylint: disable=protected-access
    ).load_sql_into_store(
        self,
        self.scenario,
        in_all_scenarios,
        truncate,
        url,
        query,
        username,
        password,
        driver,
    )
