"""Tests for copy worker."""
import json
from distutils.dir_util import copy_tree
from enum import IntEnum
from pathlib import Path
from random import choice
from typing import List, NamedTuple

import pytest
from _pytest.fixtures import SubRequest
from _pytest.tmpdir import TempdirFactory
from pytestqt.qtbot import QtBot

from tsl.copy_worker import CopyWorker

# pylint: disable=protected-access


class FileInfo(NamedTuple):
    """FileInfo."""

    filename: str
    absolute_path: Path
    relative_path: Path
    hash_value: str


class CreateDestinationFileStructure(IntEnum):
    """CreateDestinationFileStructure."""

    SOURCE_PATH = 0
    DESTINATION_PATH = 1


@pytest.fixture(name="source_path", scope="class")
def fixture_source_path(tmpdir_factory: TempdirFactory) -> Path:
    """Fixture create source directory."""
    return Path(tmpdir_factory.mktemp("source"))


@pytest.fixture(name="destination_path", scope="class")
def fixture_destination_path(tmpdir_factory: TempdirFactory) -> Path:
    """Fixture create destination directory."""
    return Path(tmpdir_factory.mktemp("destination"))


@pytest.fixture(name="copy_worker", scope="class")
def fixture_copy_worker(
    source_path: Path, destination_path: Path
) -> CopyWorker:
    """Create and return an updater."""
    copy_worker = CopyWorker(destination_path, source_path)
    copy_worker._app_name = "Toolbox"
    return copy_worker


class TestCopyWorkerBasic:
    """Test class for copy worker basics."""

    @staticmethod
    def test_copy_worker_init_source_path(
        copy_worker: CopyWorker, source_path: Path
    ) -> None:
        """Test copy worker src path."""
        assert copy_worker._source_path == source_path

    @staticmethod
    def test_copy_worker_init_dest_path(
        copy_worker: CopyWorker, destination_path: Path
    ) -> None:
        """Test copy worker dst path."""
        assert copy_worker._destination_path == destination_path

    @staticmethod
    def test_exe_path(copy_worker: CopyWorker) -> None:
        """Test copy get exe path."""
        assert copy_worker._app_name
        assert (
            copy_worker.exe_path
            == copy_worker._destination_path / copy_worker._app_name
        )


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
def test_copy_file(
    destination_path: Path, folder_structure: List[FileInfo]
) -> None:
    """Test copy file."""
    file_info: FileInfo = choice(folder_structure)
    dst_file = destination_path / file_info.filename
    CopyWorker.copy_file(dst_file, file_info.absolute_path)
    assert dst_file.exists()


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
def test_copy_file_permission_error(
    qtbot: QtBot, destination_path: Path, folder_structure: List[FileInfo]
) -> None:
    """Test copy file with permission error."""
    with qtbot.captureExceptions() as exceptions:
        file_info: FileInfo = choice(folder_structure)
        dst_file = destination_path / file_info.relative_path
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        if not dst_file.exists():
            dst_file.touch(777)  # set file read only
        with pytest.raises(PermissionError):
            CopyWorker.copy_file(dst_file, file_info.absolute_path, 1)
        assert dst_file.exists()
    assert not exceptions


@pytest.fixture(name="folder_structure", scope="class")
def fixture_folder_structure(
    request: SubRequest, source_path: Path, destination_path: Path
) -> List[FileInfo]:
    """
    Create the folder structure for the given path.

    Via the SubRequest Parameter the folder structure can be created on
    source or destination path with or without update.json file.
    """
    # path where to create the folder structure
    if request.param == CreateDestinationFileStructure.SOURCE_PATH:
        path = source_path
    else:
        path = destination_path

    files: List[FileInfo] = []
    for file in ["file1.txt", "file2.txt", "file3.txt"]:
        abs_file_path = path / file
        with abs_file_path.open("w+", encoding="utf-8") as f_handle:
            f_handle.write(file)
        file_info = FileInfo(
            file,
            abs_file_path,
            Path(file),
            CopyWorker.hash_file(abs_file_path),
        )
        files.append(file_info)

    # place folders including empty folders
    (path / "empty_folder" / "empty_folder").mkdir(parents=True)
    (path / "folder" / "folder").mkdir(parents=True)
    (path / "folder" / "empty_folder").mkdir()

    for file in ["file1.txt", "file2.txt", "file3.txt"]:
        abs_file_path = path / "folder" / "folder" / file
        with abs_file_path.open("w+", encoding="utf-8") as f_handle:
            f_handle.write(file)
        file_info = FileInfo(
            file,
            abs_file_path,
            Path("folder") / "folder" / file,
            CopyWorker.hash_file(abs_file_path),
        )
        files.append(file_info)
    return files


@pytest.fixture(name="update_json", scope="function")
def fixture_update_json(
    folder_structure: List[FileInfo], source_path: Path
) -> Path:
    """Create the update json file in the source_path."""
    file_hash = {
        str(file.relative_path): file.hash_value for file in folder_structure
    }
    with (source_path / "update.json").open("w+", encoding="utf-8") as outfile:
        json.dump({"name": "App", "files": file_hash}, outfile)

    return source_path / "update.json"


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.DESTINATION_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("folder_structure")
class TestCopyWorkerRemoveFiles:
    """Test class for copy remove functions."""

    @staticmethod
    @pytest.fixture(name="remove_empty_folders", scope="class", autouse=True)
    def fixture_remove_empty_folder(copy_worker: CopyWorker) -> List[Path]:
        """Call remove_empty_folders and return folders that are to be kept."""
        all_folders = list(copy_worker._destination_path.glob("**"))
        # find all empty folders by the used name
        empty_folders = [
            item for item in all_folders if item.name == "empty_folder"
        ]
        keep_folders = [
            item for item in all_folders if item not in empty_folders
        ]
        copy_worker._remove_empty_folders()
        return keep_folders

    @staticmethod
    def test_remove_empty_folders(
        copy_worker: CopyWorker, remove_empty_folders: List[Path]
    ) -> None:
        """Test remove empty folders."""
        assert (
            remove_empty_folders.sort()
            == list(copy_worker._destination_path.glob("**")).sort()
        )

    @staticmethod
    def test_check_files(
        copy_worker: CopyWorker,
        folder_structure: List[FileInfo],
    ) -> None:
        """Check that files are still available."""
        path_objects = list(copy_worker._destination_path.glob("**/*"))
        for item in folder_structure:
            assert Path(item.absolute_path) in path_objects


@pytest.fixture(name="file_to_remove", scope="class")
def fixture_file_to_remove(folder_structure: List[FileInfo]) -> FileInfo:
    """Return a file from the folder structure to remove."""
    return choice(folder_structure)


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.DESTINATION_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("folder_structure")
class TestRemoveFiles:
    """Test removing a file that is obsolete with the new version."""

    @staticmethod
    @pytest.fixture(name="remove_files", scope="class", autouse=True)
    @pytest.mark.usefixtures("source_path")
    def fixture_remove_files(
        copy_worker: CopyWorker,
        folder_structure: List[FileInfo],
        file_to_remove: FileInfo,
    ) -> None:
        """Test remove files with name file1."""
        copy_worker._file_list = [
            (Path(""), item.absolute_path)
            for item in folder_structure
            if item is not file_to_remove
        ]
        copy_worker._remove_files()

    @staticmethod
    def test_remove_files(file_to_remove: FileInfo) -> None:
        """Test that the file to remove was removed."""
        assert not file_to_remove.absolute_path.exists()

    @staticmethod
    def test_other_files_still_present(
        folder_structure: List[FileInfo],
        file_to_remove: FileInfo,
    ) -> None:
        """Test files are still present that should not have been removed."""
        assert [
            item.absolute_path.exists()
            for item in folder_structure
            if item is not file_to_remove
        ]


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
def test_generate_file_list(
    copy_worker: CopyWorker,
    folder_structure: List[FileInfo],
) -> None:
    """Test generate file list."""
    # setting the destination path to source path is easier to compare the
    # results
    copy_worker._destination_path = copy_worker._source_path
    copy_worker._generate_file_list()
    assert len(folder_structure) == len(copy_worker._file_list)
    for item in folder_structure:
        assert (
            item.absolute_path,
            item.absolute_path,
        ) in copy_worker._file_list


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("update_json")
def test_parse_json(
    copy_worker: CopyWorker,
    folder_structure: List[FileInfo],
) -> None:
    """Test parse json."""
    file_hash = {
        str(item.absolute_path): item.hash_value for item in folder_structure
    }
    copy_worker._parse_json()

    assert copy_worker._app_name == "App.exe"
    # comparing the dicts with hashes
    src_hash = {
        str(key): value for key, value in copy_worker._src_files.items()
    }
    assert json.dumps(src_hash, sort_keys=True) == json.dumps(
        file_hash, sort_keys=True
    )


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("update_json")
def test_parse_json_file_list(
    copy_worker: CopyWorker,
    folder_structure: List[FileInfo],
) -> None:
    """Test parse json file list."""
    file_info = folder_structure
    copy_worker._parse_json()
    assert len(file_info) == len(copy_worker._file_list)

    for idx, file in enumerate(file_info):
        assert file.absolute_path == copy_worker._file_list[idx][0]
        assert (
            copy_worker._destination_path / file.relative_path
            == copy_worker._file_list[idx][1]
        )


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("folder_structure")
@pytest.mark.usefixtures("update_json")
def test_reduce_file_list_no_files_in_dest(
    copy_worker: CopyWorker,
) -> None:
    """
    Test reduce file list for the case that destination folder is empty.

    In this case all files need to be copied.
    """
    copy_worker._parse_json()
    file_list = copy_worker._file_list.copy()
    # since all files are needed there's no change in the list
    copy_worker._reduce_file_list()
    assert file_list == copy_worker._file_list


@pytest.mark.parametrize("use_hash_file", (True, False))
@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("folder_structure")
@pytest.mark.usefixtures("update_json")
def test_reduce_file_list_same_files_in_dest(
    copy_worker: CopyWorker,
    use_hash_file: bool,
) -> None:
    """
    Test reduce file list for the case that all files exist.

    In this case no files need to be copied.
    """
    copy_tree(
        str(copy_worker._source_path), str(copy_worker._destination_path)
    )
    copy_worker._parse_json()
    if not use_hash_file:
        copy_worker._src_files = {}
    copy_worker._reduce_file_list()
    # since no files need to be copied copy worker's file list must be empty
    assert not copy_worker._file_list


@pytest.mark.parametrize("remove_files", (True, False))
@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("update_json")
def test_reduce_file_list_not_different_not_all_in_dest(
    copy_worker: CopyWorker,
    folder_structure: List[FileInfo],
    remove_files: bool,
) -> None:
    """
    Test reduce file list for the case that not all files are available.

    If remove file is true the files in dest are removed
    If remove file is false the hashes of the files are changed
    """
    # do not use every second file in dest
    files_not_available: List[Path] = []
    for idx, file in enumerate(folder_structure):
        if idx % 2 == 0:
            files_not_available.append(file.relative_path)

    copy_tree(
        str(copy_worker._source_path), str(copy_worker._destination_path)
    )
    copy_worker._parse_json()
    if remove_files:
        # remove files in dest dir
        for rel_path in files_not_available:
            (copy_worker._destination_path / rel_path).unlink()
    else:
        # change the file hash
        for rel_path in files_not_available:
            # change the hash of the source file
            copy_worker._src_files[
                copy_worker._source_path / rel_path
            ] = "1234"

        copy_worker._reduce_file_list()
        # check that the missing files (files to be copied) are among the
        # file list
        for rel_path in files_not_available:
            dest_file = copy_worker._destination_path / rel_path
            assert any(dest_file == file[1] for file in copy_worker._file_list)


@pytest.mark.parametrize(
    "folder_structure",
    [CreateDestinationFileStructure.SOURCE_PATH],
    indirect=True,
)
@pytest.mark.usefixtures("folder_structure")
@pytest.mark.usefixtures("update_json")
def test_start_copy(
    copy_worker: CopyWorker,
    qtbot: QtBot,
) -> None:
    """Test start copy function."""
    with qtbot.waitSignal(copy_worker.copy_finished):
        copy_worker.start_copy()
        file_list = copy_worker._file_list
        for item in file_list:
            assert item[1].exists()
