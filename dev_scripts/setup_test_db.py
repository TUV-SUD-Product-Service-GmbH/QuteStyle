"""
Script to setup the test database for unit tests.

This script needs the MSSQL Express Server installed and running.
"""
from tsl.dev.dev_functions import create_test_dbs

if __name__ == '__main__':
    create_test_dbs(["pse_test_db", "edoc_test_db"])