"""Test cases for tsl.init.init()."""
import os

from tsl.init import _check_install_update


# pylint: disable=protected-access, unused-argument
def test_check_install_update_no_update(monkeypatch):
    """Test that update is cancelled when UPDATE folder does not exist."""
    def _check_ide_stub(*args):
        return "test.exe"

    monkeypatch.setattr(os.path, 'abspath', _check_ide_stub)

    _check_install_update("test")
