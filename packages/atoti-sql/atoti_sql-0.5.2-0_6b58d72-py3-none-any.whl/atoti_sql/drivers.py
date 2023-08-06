"""Supported SQL drivers.

To use another JDBC driver, add the driver's JAR in the ``extra_jars`` parameter passed to :func:`atoti.config.create_config`.
"""


H2 = "org.h2.Driver"
"""H2 driver."""

IBM_DB2 = "com.ibm.db2.jcc.DB2Driver"
"""IBM DB2 driver."""

MARIADB = "org.mariadb.jdbc.Driver"
"""MariaDB driver."""

MYSQL = "com.mysql.cj.jdbc.Driver"
"""MySQL driver."""

ORACLE = "oracle.jdbc.OracleDriver"
"""Oracle driver."""

POSTGRESQL = "org.postgresql.Driver"
"""PostgreSQL driver."""

MICROSOFT_SQL_SERVER = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
"""Microsoft SQL Server driver."""


_DRIVER_PER_PATH = {
    "h2": H2,
    "db2": IBM_DB2,
    "mysql": MYSQL,
    "mariadb": MARIADB,
    "oracle": ORACLE,
    "postgresql": POSTGRESQL,
    "sqlserver": MICROSOFT_SQL_SERVER,
}


def _infer_driver(url: str) -> str:
    """Return the driver inferred from the passed URL."""
    parts = url.split(":")  # first part should always be jdbc
    potential_driver = parts[1]
    if potential_driver in _DRIVER_PER_PATH:
        return _DRIVER_PER_PATH[potential_driver]
    raise ValueError("No driver provided and cannot infer it from URL.")
