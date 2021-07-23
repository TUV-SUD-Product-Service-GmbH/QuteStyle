"""Common db stuff."""
import logging
import os
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TypeDecorator, Unicode
from sqlalchemy.engine import Dialect, Engine, create_engine
from sqlalchemy.pool import StaticPool

from tsl.init import check_ide
from tsl.vault import Vault

log = logging.getLogger("tsl.common_db")  # pylint: disable=invalid-name

# add typing that is used only when running type check
# this does not work during normal execution
if TYPE_CHECKING:
    StrEngine = TypeDecorator[str]  # noqa  # pragma: no cover
else:
    StrEngine = TypeDecorator


# pylint: disable=abstract-method, too-few-public-methods
class NullUnicode(StrEngine):
    """
    Handles NULL values for strings like empty strings.

    Please note that Column definitions must (and also should) always include
    the following: nullable=False, default="".
    """

    impl = Unicode

    # pylint: disable=no-self-use
    def process_result_value(self, value: Optional[str], _: Dialect) -> str:
        """Return the value or an empty str if the value is None (NULL)."""
        return value or ""


def create_db_engine(
    app: Vault.Application, env: Vault.Environment = None
) -> Engine:
    """Create a database engine for the given application."""
    if check_ide():
        # only print for debug purposes in IDE!
        print(
            "Creating Engine for Application: {} with Environment {}".format(
                app, env
            )
        )
    if not env:
        env_name = os.getenv(
            f"{app.name}_ENV", "DEV" if check_ide() else "PROD"
        )
        env = Vault.Environment[env_name]
        if check_ide():
            # only print for debug purposes in IDE!
            print("Environment for Engine: " + env.name)
    conn_str = Vault.return_conn_str(app, env)
    # pre pool ping will ensure, that connection is reestablished if not alive
    # check_same_thread and poolclass are necessary so that unit test can use a
    # in memory sqlite database across different threads.
    engine = create_engine(
        "mssql+pyodbc:///?odbc_connect=" + conn_str,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        pool_pre_ping=True,
    )
    if check_ide():
        # only print for debug purposes in IDE!
        print("Created engine for {}: {}".format(app, engine))
    return engine
