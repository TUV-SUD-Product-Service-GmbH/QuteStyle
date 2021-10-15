"""Common db stuff."""
import logging
import os
from typing import Optional, Type

from pyodbc import Connection
from sqlalchemy import TypeDecorator, Unicode, event
from sqlalchemy.engine import Dialect, Engine, create_engine
from sqlalchemy.pool import QueuePool, StaticPool
from sqlalchemy.pool.base import _ConnectionFairy, _ConnectionRecord

from tsl.init import check_ide
from tsl.vault import Vault

log = logging.getLogger("tsl.common_db")  # pylint: disable=invalid-name


class NullUnicode(TypeDecorator):  # pylint: disable=abstract-method
    """
    Handles NULL values for strings like empty strings.

    Please note that Column definitions must (and also should) always include
    the following: nullable=False, default="".
    """

    impl = Unicode

    def process_result_value(  # pylint: disable=no-self-use
        self, value: Optional[str], _: Dialect
    ) -> str:
        """Return the value or an empty str if the value is None (NULL)."""
        return value or ""

    @property
    def python_type(self) -> Type[str]:
        """Return the type expected by instances of this type."""
        return str


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

    # From SqlAlchemyDoc -> QueuePool is the default pooling implementation
    # used for all Engine objects, unless the SQLite dialect is in use.

    # use QueuePool for PROD. Handle parallel execution of sql requests.
    # The pool holds a set of 5 connections which are shared across requests
    # 5 is the default setting so keep this setting here
    if env_name == "PROD":
        print("Use engine with poolclass queue pool")
        engine = create_engine(
            "mssql+pyodbc:///?odbc_connect=" + conn_str,
            connect_args={"check_same_thread": False},
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=0,
            pool_pre_ping=True,
        )
        event.listen(engine, "checkout", receive_checkout)
        event.listen(engine, "checkin", receive_checkin)
    else:
        print("Use engine with poolclass StaticPool")
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


def receive_checkout(
    conn: Connection, _: _ConnectionRecord, __: _ConnectionFairy
) -> None:
    """Checkout a pooled connection."""
    log.debug("Checkout pooled connection %s.", conn)


def receive_checkin(conn: Connection, _: _ConnectionRecord) -> None:
    """Checkin a pooled connection."""
    log.debug("Checkin pool connection %s.", conn)
