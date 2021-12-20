"""Development functions."""
from __future__ import annotations

import json
import pickle
import re
import subprocess
import sys
import xml.etree.cElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import pyodbc
from PyQt5 import uic  # pylint: disable=wrong-import-order

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
    proc_path = Path(__file__).parent / "test_procedures"
    for file in proc_path.iterdir():
        with file.open(encoding="utf-8") as fhandle:
            escaped_sql = fhandle.read()
            print("Creating procedure " + file.stem)
            cursor.execute(escaped_sql)

    connection.close()


def compile_ui_files(src_folders: List[Path]) -> None:
    """
    Compile the ui files.

    Compile the ui files in src_folders and copy the created
    files to gen folder.
    """
    for folder in src_folders:
        for file in folder.iterdir():
            print(f"Converting file {file}")
            with file.open("r", encoding="utf-8") as source:
                new_file = file.parent.parent / "gen" / f"ui_{file.stem}.py"
                with new_file.open(
                    "w",
                    encoding="utf-8",
                ) as target:
                    uic.compileUi(source, target)
        # run black after ui files are created
        subprocess.run(
            [
                Path(sys.executable).parent / "black",
                "-l79",
                folder.parent / "gen",
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


def get_sorted_version_directories(changelog_path: Path) -> List[Path]:
    """Get all version directories and return them sorted as list."""
    directories = [item for item in changelog_path.iterdir() if item.is_dir()]
    sorted_directories = sorted(
        directories,
        reverse=True,
        key=lambda x: tuple(map(int, x.name.split("."))),
    )
    return sorted_directories


# key = widget class name
# values = changelogs for widget according to language (de/en)
WidgetLogInfo = Dict[str, List[Dict[str, str]]]


def list_dd() -> Dict[Any, List[Any]]:
    """
    Module level method to allow pickling of defaultdict.

    See: https://stackoverflow.com/questions/16439301/cant-pickle-defaultdict
    """
    return defaultdict(list)


def get_change_log_data(
    app_name: str,
    change_log_path: Path,
) -> Dict[str, WidgetLogInfo]:
    """Read in all the changelog data per version."""
    print("Get changelog data")
    change_log_data: Dict[str, WidgetLogInfo] = defaultdict(list_dd)
    sorted_directories = get_sorted_version_directories(change_log_path)
    for version in sorted_directories:
        for file in version.glob("*.json"):
            try:
                widget, texts = _parse_change_log(file)
            except NotImplementedError:
                continue
            change_log_data[version.name][widget or app_name].append(texts)
    return dict(change_log_data)


def _parse_change_log(file: Path) -> Tuple[str, Dict[str, str]]:
    """Parse the widget name and the change log texts from a JSON file."""
    with file.open(encoding="utf-8") as handle:
        entry = json.loads(handle.read())
    if isinstance(entry, List):
        # old changelog data was stored as list. Do not add to logs
        raise NotImplementedError(
            "Parsing of old changelogs isn't implemnentd"
        )
    text = _parse_str(entry, "text")
    widget = _parse_str(entry, "widget")
    text_en = _parse_str(entry, "text_en")

    return widget, {"de": text, "en": text_en}


def _parse_str(entry: Dict[Any, Any], key: str) -> str:
    """Parse the text for the given key from the entry (dict from JSON)."""
    try:
        text = entry[key]
        assert isinstance(text, str)
    except KeyError as error:
        # in case entry is not available an exception is thrown
        print(f"Entry in log not found: {key}")
        raise KeyError from error
    except AssertionError as error:
        print(f"Entry has invalid type: {key}")
        raise KeyError from error
    return text


def _create_resource_file(  # pylint: disable=too-many-locals
    resource_file_path: Path,
    change_log_path: Path,
    change_log_data: Dict[str, WidgetLogInfo],
) -> None:
    """Create the resource file from data."""
    print("Creating new resources.qrc")
    resource_file = resource_file_path / "resources.qrc"
    resource_py = resource_file_path / "resources_cl.py"
    resource_file.unlink(True)

    # Store the changelog data (serialize)
    print("Store the changelog data ")
    change_log_data_path = resource_file_path / "change_log_data.pickle"
    with change_log_data_path.open("wb") as handle:
        pickle.dump(change_log_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    rcc = ET.Element("RCC")
    qrc = ET.SubElement(rcc, "qresource")
    ET.SubElement(qrc, "file").text = "change_log_data.pickle"

    # store added images in the resource file. Images are extracted from text
    # and text_en
    added_images = set()
    for version_data in change_log_data.values():
        for log_data in version_data.values():
            for lang in log_data:
                images = re.findall('src=":([^"]+)"', lang["de"])
                added_images.update(list(images))
                images = re.findall('src=":([^"]+)"', lang["en"])
                added_images.update(list(images))

    for image in added_images:
        image_path = Path(change_log_path).joinpath(image)
        ET.SubElement(qrc, "file", {"alias": image}).text = str(
            image_path.relative_to(Path.cwd()).as_posix()
        )
    tree = ET.ElementTree(rcc)
    tree.write(resource_file)

    print("Generating resource_rc.py with new resources.qrc")
    assert subprocess.call(f"PyRCC5 -o {resource_py} {resource_file}") == 0

    print("Deleting resources.qrc")
    resource_file.unlink()
    print("Delete dict data")
    change_log_data_path.unlink()


def generate_changelog_resource_file(
    app_name: str,
    change_log_path: Path,
    resource_file_path: Path,
) -> None:
    """
    Generate changelog resource file.

    app_name: Name of the application
    change_log_path: changelog path
    resource_file_path: path where the resource file should be stored
    """
    print("Generate changelog resource file")
    change_log_data = get_change_log_data(app_name, change_log_path)
    _create_resource_file(resource_file_path, change_log_path, change_log_data)
