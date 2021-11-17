"""
TSL vault to retrieve connection strings for our applications.

You can get a valid connection string by providing app (Vault.Application) and
env (Vault.Environment) to Vault.return_conn_str().

It is intended that this class will be connected to our KeyVault to retrieve
the secrets and not store them in the code.
"""
import logging
import os
import urllib.parse
from enum import Enum
from typing import Dict

from tsl.init import check_ide

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name


class Vault:
    """Vault to store database connection secrets."""

    class Environment(Enum):
        """Enumeration for the different environments."""

        DEV = 1
        TEST = 2
        PROD = 3

    class Application(Enum):
        """Enumeration for the different applications."""

        EDOC = 0
        PSE = 1  # currently not used, but PSE and EDOC will be separated.
        CHEMUP = 2
        LABMONITOR = 3
        TOOLBOX = 4

    CREATED_DATABASES: Dict[Application, Environment] = {}

    @staticmethod
    def local_conn_str() -> str:  # pragma: no cover
        """
        Return the connection string to the local database.

        If the environment variable PIPELINE is set to 1, the database path is
        returned for usage in the PIPELINE.

        This method can't be tested since we would need to mock getenv that is
        needed for the test.
        """
        if os.getenv("PIPELINE") == "1":
            return (
                r"Driver={ODBC Driver 17 for SQL Server};"
                r"Server=(localdb)\mssqllocaldb;"
                r"Trusted_Connection=yes;"
            )
        return (
            r"Driver={ODBC Driver 17 for SQL Server};"
            r"Server=localhost\SQLEXPRESS;"
            r"Trusted_Connection=yes;"
        )

    @staticmethod
    def return_conn_str(app: Application, env: Environment) -> str:
        """Return the connection string for the app and environment."""
        log.debug("Getting db connection for app %s on env %s", app, env)
        # All connection strings should be requested only once per lifecycle.
        assert app not in Vault.CREATED_DATABASES
        Vault.CREATED_DATABASES[app] = env
        appn = app.name

        driver = os.getenv(
            f"{appn}_DB_DRIVER", "ODBC Driver 17 for SQL Server"
        )
        server = os.getenv(f"{appn}_DB_SERVER", Vault._get_server(app, env))
        user = os.getenv(f"{appn}_DB_USER", Vault._get_user(app, env))
        password = os.getenv(f"{appn}_DB_USER", Vault._get_password(app, env))
        if "+" in password or ";" in password:
            raise ValueError("Password MUST not contain a '+' or ';'.")
        name = os.getenv(f"{appn}_DB_NAME", Vault._get_name(app, env))

        conn_str = f"Driver={{{driver}}};" f"Server={server};"
        if user:
            conn_str += f"uid={user};pwd={password};"
        else:
            conn_str += "Trusted_Connection=yes;"
        conn_str += f"Database={name};"
        if (
            app in (Vault.Application.EDOC, Vault.Application.PSE)
            and env != Vault.Environment.DEV
        ):
            conn_str += "MultiSubnetFailover=yes;"
        if env != Vault.Environment.DEV:
            conn_str += "Encrypt=yes;TrustServerCertificate=yes"
        if check_ide():
            # only print for debug purposes in IDE!
            print("Returning " + conn_str)
        return urllib.parse.quote(conn_str)

    @staticmethod
    def _get_server(app: Application, env: Environment) -> str:
        """Return the default server for the app in the environment."""
        if os.getenv("PIPELINE") == "1" and env == Vault.Environment.DEV:
            return r"(localdb)\mssqllocaldb;"
        server = {
            Vault.Application.EDOC: {
                Vault.Environment.DEV: r"localhost\SQLEXPRESS",
                Vault.Environment.TEST: "10.40.172.122",
                Vault.Environment.PROD: "psexplorerhost.muc.de.itgr.net",
            },
            Vault.Application.PSE: {
                Vault.Environment.DEV: r"localhost\SQLEXPRESS",
                Vault.Environment.TEST: "10.40.172.122",
                Vault.Environment.PROD: "psexplorerhost.muc.de.itgr.net",
            },
            Vault.Application.CHEMUP: {
                Vault.Environment.DEV: r"localhost\SQLEXPRESS",
                Vault.Environment.TEST: "chemup-test.database.windows.net",
                Vault.Environment.PROD: "ASQL0050",
            },
            Vault.Application.LABMONITOR: {
                Vault.Environment.DEV: r"localhost\SQLEXPRESS",
                Vault.Environment.TEST: "sdegbma07043",
                Vault.Environment.PROD: "sdegbma07043",
            },
            Vault.Application.TOOLBOX: {
                Vault.Environment.DEV: r"localhost\SQLEXPRESS",
                Vault.Environment.TEST: "chemup-test.database.windows.net",
                Vault.Environment.PROD: "ASQL0040",
            },
        }[app][env]
        if env != Vault.Environment.DEV:
            server += ",1433"
        return server

    @staticmethod
    def _get_user(app: Application, env: Environment) -> str:
        """Return the default user for the app in the environment."""
        return {
            Vault.Application.EDOC: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "lv_edoc",
                Vault.Environment.PROD: "lv_edoc",
            },
            Vault.Application.PSE: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "lv_edoc",
                Vault.Environment.PROD: "lv_edoc",
            },
            Vault.Application.CHEMUP: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "chemup",
                Vault.Environment.PROD: "ps_chemup",
            },
            Vault.Application.LABMONITOR: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "ldpTest",
                Vault.Environment.PROD: "ldpPRODsec",
            },
            Vault.Application.TOOLBOX: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "chemup",
                Vault.Environment.PROD: "pscps",
            },
        }[app][env]

    @staticmethod
    def _get_password(app: Application, env: Environment) -> str:
        """Return the default password for the app in the environment."""
        return {
            Vault.Application.EDOC: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "hooters",
                Vault.Environment.PROD: "hooters",
            },
            Vault.Application.PSE: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "hooters",
                Vault.Environment.PROD: "hooters",
            },
            Vault.Application.CHEMUP: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: r"Zu8LU3fAriFz6x59",
                Vault.Environment.PROD: "u6()D#[[$8G2v5b-",
            },
            Vault.Application.LABMONITOR: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: "Kt5B7§]O5e6!m7AQ",
                Vault.Environment.PROD: "d{Djh<33B*nY1)F2",
            },
            Vault.Application.TOOLBOX: {
                Vault.Environment.DEV: "",
                Vault.Environment.TEST: r"Zu8LU3fAriFz6x59",
                Vault.Environment.PROD: r"8E51(JLC2sY<",
            },
        }[app][env]

    @staticmethod
    def _get_name(app: Application, env: Environment) -> str:
        """Return the default db name for the app in the environment."""
        return {
            Vault.Application.EDOC: {
                Vault.Environment.DEV: "edoc_test_db",
                Vault.Environment.TEST: "EDOC",
                Vault.Environment.PROD: "EDOC",
            },
            Vault.Application.PSE: {
                Vault.Environment.DEV: "pse_test_db",
                Vault.Environment.TEST: "PSExplorer",
                Vault.Environment.PROD: "PSExplorer",
            },
            Vault.Application.CHEMUP: {
                Vault.Environment.DEV: "chemup_test_db",
                Vault.Environment.TEST: "chemup_test_db",
                Vault.Environment.PROD: "PS_ChemUp",
            },
            Vault.Application.LABMONITOR: {
                Vault.Environment.DEV: "ldp_server_test",
                Vault.Environment.TEST: "ldp_server_test",
                Vault.Environment.PROD: "ldp_server",
            },
            Vault.Application.TOOLBOX: {
                Vault.Environment.DEV: "cps_test_db",
                Vault.Environment.TEST: "cps-test-db",
                Vault.Environment.PROD: "PS_CPS",
            },
        }[app][env]
