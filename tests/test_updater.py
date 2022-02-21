"""Tests for updater."""
import json
import string
from pathlib import Path
from random import choice, randint
from typing import Optional, Tuple

import pytest
from _pytest.fixtures import SubRequest
from _pytest.monkeypatch import MonkeyPatch

from tsl.dev.mocks import check_call
from tsl.update_window import AppData
from tsl.updater import Updater

# pylint: disable=protected-access


def random_str(length: int = 10) -> str:
    """Return a random str with the given length."""
    return "".join(
        choice(string.ascii_uppercase + string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


@pytest.fixture(name="app_name", scope="session")
def fixture_app_name() -> str:
    """Return a random app name."""
    return random_str()


@pytest.fixture(name="version_tuple", scope="session")
def fixture_version_tuple() -> Tuple[int, int, int]:
    """Return a random version as tuple."""
    return randint(0, 9), randint(0, 9), randint(0, 9)


@pytest.fixture(name="version", scope="session")
def fixture_version(version_tuple: Tuple[int, int, int]) -> str:
    """Return a random version."""
    return ".".join(map(str, version_tuple))


@pytest.fixture(name="app_data", scope="session")
def fixture_app_data(version: str, app_name: str) -> AppData:
    """Return AppData for tests."""
    return AppData(app_name, version)


@pytest.fixture(name="updater", scope="function")
def fixture_updater(app_data: AppData) -> Updater:
    """Create and return an updater."""
    return Updater(app_data)


@pytest.fixture(name="update_json", scope="function")
def fixture_update_json(
    request: SubRequest, app_data: AppData, tmp_path: Path
) -> Path:
    """Create update json file."""
    if request.param:
        # extend the last value of the provided version string
        version_list = app_data.app_version.split(".")
        version_list[2] += "0"
        version = ".".join(version_list)
    else:
        version = app_data.app_version

    update_path = tmp_path / app_data.app_name / "TSL-UPDATE"
    update_path.mkdir(parents=True)
    with open(update_path / "update.json", "w+", encoding="utf-8") as outfile:
        json.dump({"version": version}, outfile)
    return update_path / "update.json"


def test_update_window_init(updater: Updater, app_data: AppData) -> None:
    """Test Update window init."""
    assert updater._update_available is False
    assert updater.app_data.app_name == app_data.app_name
    assert updater.app_data.app_version == app_data.app_version


def test_start_update(updater: Updater) -> None:
    """Test the start update function."""
    with check_call(Updater, "_check_for_update", True):
        updater.run()
        assert updater._update_available is True


@pytest.mark.parametrize("return_value", [Path("")])
def test_check_update_path_not_available(
    updater: Updater, return_value: Optional[str]
) -> None:
    """Test check for update with None return as path."""
    with check_call(Updater, "get_accessible_path", return_value):
        assert updater._check_for_update() is False


@pytest.mark.parametrize(
    "update_json",
    [False],
    indirect=True,
)
@pytest.mark.usefixtures("update_json")
def test_check_update_no_update(
    updater: Updater,
    tmp_path: Path,
) -> None:
    """Test that update is not running when only same version is available."""
    with check_call(Updater, "get_accessible_path", tmp_path):
        assert updater._check_for_update() is False


@pytest.mark.parametrize(
    "update_json",
    [True],
    indirect=True,
)
@pytest.mark.usefixtures("update_json")
def test_check_update_update(
    updater: Updater,
    tmp_path: Path,
) -> None:
    """Test that update is running for different versions."""
    with check_call(Updater, "get_accessible_path", tmp_path):
        assert updater._check_for_update() is True


@pytest.mark.parametrize(
    "update_json",
    [False],
    indirect=True,
)
def test_extract_json_version(
    updater: Updater, update_json: Path, app_data: AppData
) -> None:
    """Test extract json version."""
    assert updater._extract_version(update_json) == app_data.app_version


def test_get_accessible_path_na(
    updater: Updater, monkeypatch: MonkeyPatch
) -> None:
    """Test get accessible path function with not available path."""
    monkeypatch.setattr("tsl.updater.LAGER_PATHS", "")
    with pytest.raises(ValueError):
        assert updater.get_accessible_path()


def test_get_accessible_path(
    updater: Updater, monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Test get accessible path function."""
    base_path = tmp_path / "test"
    base_path.mkdir()
    monkeypatch.setattr("tsl.updater.LAGER_PATHS", ("", base_path))
    assert updater.get_accessible_path() == base_path


@pytest.mark.parametrize("update_available", (True, False))
def test_exit_application_state(
    updater: Updater, update_available: bool
) -> None:
    """Test exit application state."""
    updater._update_available = update_available
    assert updater.exit_application is update_available
