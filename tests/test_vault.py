"""Tests for the Vault."""
import pytest

from tsl.vault import Vault


def test_all() -> None:
    """A simple test that will check if all conn_strs returned are valid."""
    for env in Vault.Environment:
        # Clear the CREATED_DATABASES so that we can test for other env again.
        Vault.CREATED_DATABASES.clear()
        for app in Vault.Application:
            assert Vault.return_conn_str(app, env)
            with pytest.raises(AssertionError):
                # Trying to get a connection str twice MUST fail.
                assert Vault.return_conn_str(app, env)
