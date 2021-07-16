"""Tests for the Vault."""
from tsl.vault import Vault


def test_all() -> None:
    """A simple test that will check if all conn_strs returned are valid."""
    for env in Vault.Environment:
        for app in Vault.Application:
            assert Vault.return_conn_str(app, env)
