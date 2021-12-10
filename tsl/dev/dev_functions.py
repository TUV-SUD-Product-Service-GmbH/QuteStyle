"""Development functions."""
import json
import ntpath
import os
import pickle
import re
import subprocess
import sys
import xml.etree.cElementTree as ET
from typing import Dict, Iterable, List

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
    proc_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_procedures"
    )
    for file in os.listdir(proc_path):
        with open(os.path.join(proc_path, file), encoding="utf-8") as fhandle:
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
            print(f"Converting file {file}")
            new_file = "ui_" + file.replace(".ui", "") + ".py"
            with open(
                os.path.join(folder, file), "r", encoding="utf-8"
            ) as source:
                with open(
                    os.path.join(os.path.dirname(folder), "gen", new_file),
                    "w",
                    encoding="utf-8",
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


def get_sorted_version_directories(changelog_path: str) -> List[str]:
    """Get all version directories and return them sorted as list."""
    directories = [
        name
        for name in os.listdir(changelog_path)
        if os.path.isdir(os.path.join(changelog_path, name))
    ]
    sorted_directories = sorted(
        directories,
        reverse=True,
        key=lambda x: tuple(map(int, x.split("."))),
    )
    return sorted_directories


# key = widget class name
# values = changelogs for widget according to language (de/en)
WidgetLogInfo = Dict[str, List[Dict[str, str]]]


def get_change_log_data(
    app_name: str,
    change_log_path: str,
) -> Dict[str, WidgetLogInfo]:
    """Read in all the changelog data per version."""
    print("Get changelog data")
    change_log_data: Dict[str, WidgetLogInfo] = {}
    sorted_directories = get_sorted_version_directories(change_log_path)
    for version in sorted_directories:
        path = os.path.join(change_log_path, version)
        for file in os.listdir(path):
            if not file.endswith(".json"):
                continue
            with open(os.path.join(path, file), encoding="utf-8") as handle:
                entry = json.loads(handle.read())
            if isinstance(entry, List):
                # old changelog data was stored as list. Do not add to logs
                continue
            try:
                text = entry["text"]
                widget = entry["widget"]
            except KeyError as error:
                # in case entry is not available an exception is thrown
                print("Entry in log not found: " + os.path.join(path, file))
                raise KeyError from error

            if not widget:
                # in case widget is empty it is handled as a
                # general app log data
                widget = app_name
            try:
                text_en = entry["text_en"] or text
            except KeyError:
                # use german text in case english text is not
                # available
                text_en = text
            if version not in change_log_data:
                change_log_data[version] = {}
            try:
                change_log_data[version][widget].append(
                    {"de": text, "en": text_en}
                )
            except KeyError:
                change_log_data[version][widget] = [
                    {"de": text, "en": text_en}
                ]
    return change_log_data


def _create_resource_file(  # pylint: disable=too-many-locals
    resource_file_path: str,
    change_log_rel_path: str,
    change_log_data: Dict[str, WidgetLogInfo],
) -> None:
    """Create the resource file from data."""
    print("Creating new resources.qrc")
    resource_file = os.path.join(resource_file_path, "resources.qrc")
    resource_py = os.path.join(resource_file_path, "resources_cl.py")
    try:
        os.remove(resource_file)
    except FileNotFoundError:
        pass

    # Store the changelog data (serialize)
    print("Store the changelog data ")
    change_log_data_path = os.path.join(
        resource_file_path, "change_log_data.pickle"
    )
    with open(change_log_data_path, "wb") as handle:
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
        ET.SubElement(qrc, "file", {"alias": image}).text = os.path.join(
            change_log_rel_path, image
        )
    tree = ET.ElementTree(rcc)
    tree.write(resource_file)

    print("Generating resource_rc.py with new resources.qrc")
    assert subprocess.call(f"PyRCC5 -o {resource_py} {resource_file}") == 0

    print("Deleting resources.qrc")
    os.remove(resource_file)
    print("Delete dict data")
    os.remove(change_log_data_path)


def generate_changelog_resource_file(
    app_name: str,
    change_log_rel_path: str,
    resource_file_path: str,
) -> None:
    """
    Generate changelog resource file.

    app_name: Name of the application
    change_log_rel_path: relative path from resource_file_path to changelog
    path
    resource_file_path: path where the resource file should be stored
    """
    print("Generate changelog resource file")
    change_log_data = get_change_log_data(
        app_name, os.path.join(resource_file_path, change_log_rel_path)
    )
    _create_resource_file(
        resource_file_path, change_log_rel_path, change_log_data
    )
