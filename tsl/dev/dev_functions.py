"""Development functions."""
import ntpath
import os
import subprocess
import sys
from typing import Iterable, List

import pyodbc
from PyQt5 import uic  # type: ignore

from tsl.vault import Vault


def add_edoc_procedures() -> None:
    """
    Add the stored procedures to the edoc db.

    The procedures must be stored in a file in test/test_procedures. The name
    of the file must be the name of the stored procedure.
    """
    print("Creating EDOC procedures needed for unit tests.")
    edoc_conn_str = Vault.local_conn_str().replace(
        "Trusted_Connection=yes;",
        "DATABASE=edoc_test_db;Trusted_Connection=yes;",
    )
    print("Connection: " + edoc_conn_str)
    connection = pyodbc.connect(edoc_conn_str, autocommit=True)
    cursor = connection.cursor()

    proc_path = os.path.join("tests", "test_procedures")
    for file in os.listdir(proc_path):
        with open(os.path.join(proc_path, file)) as fhandle:
            escaped_sql = fhandle.read()
            print("Creating procedure " + file.replace(".sql", ""))
            cursor.execute(escaped_sql)

    connection.close()


def compile_ui_files(src_folders: List[str]) -> None:
    """
    Compile the ui files.

    Compile the ui files in src_folders and copy the created
    files to gen folder.
    """
    for folder in src_folders:
        for file in os.listdir(folder):
            print("Converting file {}".format(file))
            new_file = "ui_" + file.replace(".ui", "") + ".py"
            with open(os.path.join(folder, file), "r") as source:
                with open(
                    os.path.join(os.path.dirname(folder), "gen", new_file), "w"
                ) as target:
                    uic.compileUi(source, target)
        # run black after ui files are created
        subprocess.run(
            [
                os.path.join(ntpath.split(sys.executable)[0], "black"),
                "-l79",
                os.path.join(os.path.dirname(folder), "gen"),
            ],
            check=False,
        )
    print("Conversion finished")


def create_test_dbs(dbs: Iterable[str]) -> None:
    """
    Create the given test databases on the SQL Express server.

    Existing databases will be dropped.
    """
    print("Setting up server for unit tests.")
    conn_str = Vault.local_conn_str()

    conn = pyodbc.connect(conn_str, autocommit=True)
    print("Connection str: " + conn_str)
    cursor = conn.cursor()

    for db_name in dbs:
        try:
            print("Deleting database " + db_name)
            cursor.execute(f"DROP DATABASE {db_name};")
        except pyodbc.ProgrammingError as exception:
            print(str(exception))
            if exception.args[0] == "42S02":
                print("Database does not exist, cannot be deleted")
            else:
                raise
        print(f"Creating database {db_name}")
        cursor.execute(f"CREATE DATABASE {db_name};")

    if "edoc_test_db" in dbs:
        add_edoc_procedures()

    conn.close()
