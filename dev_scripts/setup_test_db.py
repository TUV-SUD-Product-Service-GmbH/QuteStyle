"""
Script to setup the test database for unit tests.

This script needs the MSSQL Express Server installed and running.
"""
import os
import pyodbc

if __name__ == '__main__':
    print("Setting up server for unit tests.")

    STD_PATH = r"Driver={ODBC Driver 17 for SQL Server};Server=(localdb)\ms" \
               r"sqllocaldb;Trusted_Connection=yes;"
    CONN_STR = os.getenv("TEST_DB_PATH", STD_PATH)

    CONN = pyodbc.connect(CONN_STR, autocommit=True)

    CURSOR = CONN.cursor()

    DB_NAMES = ["pse_test_db", "edoc_test_db"]

    for db_name in DB_NAMES:
        try:
            print("Deleting database " + db_name)
            CURSOR.execute(f"DROP DATABASE {db_name};")
        except pyodbc.ProgrammingError as exception:
            print(str(exception))
            if exception.args[0] == "42S02":
                print("Database does not exist, cannot be deleted")
            else:
                raise
        print(f"Creating database {db_name}")
        CURSOR.execute(f"CREATE DATABASE {db_name};")

    CONN.close()
