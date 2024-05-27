"""Development functions."""

# mypy: ignore-errors
from __future__ import annotations

import json
import pickle
import re
import subprocess
import sys
import xml.etree.ElementTree as ElTree
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple


def compile_ui_files(src_folders: list[Path]) -> None:
    """
    Compile the ui files.

    Compile the ui files in src_folders and copy the created
    files to gen folder.
    """
    for folder in src_folders:
        for file in folder.iterdir():
            print(f"Converting file {file}")
            target = file.parent.parent / "gen" / f"ui_{file.stem}.py"
            subprocess.run(
                [
                    Path(sys.executable).parent / "pyside6-uic",
                    "--no-autoconnection",
                    file,
                    "-o",
                    target,
                ],
                check=True,
            )
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


def get_sorted_version_directories(changelog_path: Path) -> list[Path]:
    """Get all version directories and return them sorted as list."""
    directories = [item for item in changelog_path.iterdir() if item.is_dir()]
    return sorted(
        directories,
        reverse=True,
        key=lambda x: tuple(map(int, x.name.split("."))),
    )


# key = widget class name
# values = changelogs for widget according to language (de/en)
WidgetLogInfo = dict[str, list[dict[str, str]]]


def list_dd() -> dict[Any, list[Any]]:
    """
    Implement module level method to allow pickling of defaultdict.

    See: https://stackoverflow.com/questions/16439301/cant-pickle-defaultdict
    """
    return defaultdict(list)


class VersionInfo(NamedTuple):
    """Version information."""

    version: str
    release_date: str


def get_change_log_data(
    app_name: str,
    change_log_path: Path,
) -> dict[VersionInfo, WidgetLogInfo]:
    """Read in all the changelog data per version."""
    print("Get changelog data")
    change_log_data: dict[VersionInfo, WidgetLogInfo] = defaultdict(list_dd)
    sorted_directories = get_sorted_version_directories(change_log_path)
    for version in sorted_directories:
        release_date = ""
        if Path(version / "meta.json").exists():
            release_date = _parse_meta_info(version / "meta.json")
        for file in version.glob("*[!meta].json"):
            try:
                widget, texts = _parse_change_log(file)
            except NotImplementedError:
                continue
            change_log_data[VersionInfo(version.name, release_date)][
                widget or app_name
            ].append(texts)
    return dict(change_log_data)


def _parse_meta_info(file: Path) -> str:
    """Parse the version meta information from a JSON file."""
    with file.open(encoding="utf-8") as handle:
        entry = json.loads(handle.read())
    return _parse_str(entry, "release_date")


def _parse_change_log(file: Path) -> tuple[str, dict[str, str]]:
    """Parse the widget name and the change log texts from a JSON file."""
    with file.open(encoding="utf-8") as handle:
        entry = json.loads(handle.read())
    if isinstance(entry, list):
        # old changelog data was stored as list. Do not add to logs
        raise NotImplementedError(
            "Parsing of old changelogs isn't implemented"
        )
    text = _parse_str(entry, "text")
    widget = _parse_str(entry, "widget")
    text_en = _parse_str(entry, "text_en")

    return widget, {"de": text, "en": text_en}


def _parse_str(entry: dict[Any, Any], key: str) -> str:
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
    change_log_data: dict[VersionInfo, WidgetLogInfo],
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
    rcc = ElTree.Element("RCC")
    qrc = ElTree.SubElement(rcc, "qresource")
    ElTree.SubElement(qrc, "file").text = "change_log_data.pickle"

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
        ElTree.SubElement(qrc, "file", {"alias": image}).text = str(
            image_path.relative_to(resource_file_path)
        )
    tree = ElTree.ElementTree(rcc)
    tree.write(resource_file)

    print("Generating resource_rc.py with new resources.qrc")
    assert (
        subprocess.call(f"pyside6-rcc -o {resource_py} {resource_file}") == 0
    )

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
