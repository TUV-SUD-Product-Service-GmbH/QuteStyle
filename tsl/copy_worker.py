"""Definition for CopyWorker to Update TSL apps."""
from __future__ import annotations

import filecmp
import hashlib
import json
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

from PyQt5.QtCore import QEventLoop, QObject, QTimer, pyqtSignal, pyqtSlot

log = logging.getLogger("tsl.copy_worker")  # pylint: disable=invalid-name


class CopyWorker(QObject):
    """Worker object processing an update."""

    current_file = pyqtSignal(str, name="current_file")
    files_copied = pyqtSignal(int, int, name="files_copied")
    copy_finished = pyqtSignal(name="copy_finished")
    status_changed = pyqtSignal(str, name="status_changed")

    def __init__(
        self,
        destination_path: Path,
        source_path: Path,
        parent: QObject | None = None,
    ) -> None:
        """
        Create a new CopyWorker.

        The given destination_path is the path into which the application will
        be installed.
        source_path is checked for update.json which provides the information
        which files to copy.
        """
        super().__init__(parent)
        self._source_path = source_path
        self._destination_path = destination_path
        self._app_name: str | None = None
        # stores the source files and related hash
        self._src_files: Dict[Path, str] = {}
        # stores the source and destination files
        self._file_list: List[Tuple[Path, Path]] = []
        log.debug("Destination Path: %s", self._destination_path)
        log.debug("Source Path: %s", self._source_path)

    @property
    def exe_path(self) -> Path:
        """Return the executable path of the app."""
        assert self._app_name
        return self._destination_path / self._app_name

    @pyqtSlot(name="start_copy")
    def start_copy(  # pylint: disable=too-many-branches
        self,
    ) -> None:
        """Start to copy the files from the def file to the destination."""
        self.status_changed.emit("Checking TSL definition file of update.")
        update_file = self._source_path / "update.json"
        log.debug("Checking file: %s", update_file)
        if update_file.exists():
            self.status_changed.emit("Reading TSL definition file.")
            self._parse_json()
        else:
            self.status_changed.emit("update_failed")
            if not self._source_path.exists():
                log.debug("Source path does not exist: %s", self._source_path)
            else:
                log.debug("update.json file missing in %s", self._source_path)
            return
        self.status_changed.emit(
            "Removing obsolete files from installation folder."
        )
        self._remove_files()
        self._remove_empty_folders()
        self.status_changed.emit("Calculating list of files to be copied")
        self._reduce_file_list()
        self.status_changed.emit("Copying files...")

        for idx, (src, dst) in enumerate(self._file_list):
            self.current_file.emit(str(dst))
            log.debug("Coping from %s to %s", src, dst)
            try:
                log.debug("Trying to create folder %s", dst.parent)
                dst.parent.mkdir(parents=True)
            except FileExistsError:
                log.debug("Folder does already exist")
            try:
                self.copy_file(dst, src)
            except PermissionError:
                log.debug("Permission denied for destination: %s", dst)
                self.status_changed.emit("Update failed.")
                break
            self.files_copied.emit(idx + 1, len(self._file_list))
        self.files_copied.emit(len(self._file_list), len(self._file_list))
        self.copy_finished.emit()
        self.status_changed.emit("Update complete.")

    @staticmethod
    def copy_file(dst: Path, src: Path, retries_num: int = 30) -> None:
        """Copy a file from dst to src."""
        while retries_num > 0:
            try:
                shutil.copy(src, dst)
                break
            except PermissionError:
                log.warning(
                    "Could not copy %s to %s due to PermissionError. Retry",
                    dst,
                    src,
                )
                # sleep 1 second in an event loop
                loop = QEventLoop()
                QTimer.singleShot(1000, loop.quit)
                loop.exec()
                retries_num -= 1

        if retries_num == 0:
            msg = f"Failed copy {src} to {dst} due to PermissionError"
            log.warning(msg)
            raise PermissionError(msg)

    def _remove_files(self) -> None:
        """Remove files from the path that aren't needed anymore."""
        log.debug("Deleting obsolete files")
        for file in self._destination_path.rglob("*"):
            if file.is_file():
                if not any(
                    file == dst_path for _, dst_path in self._file_list
                ):
                    log.debug("Removing file %s", file)
                    try:
                        file.unlink()
                    except PermissionError:
                        log.debug("Cannot delete file because locked.")
        log.debug("Deletion of obsolete files finished")

    def _remove_empty_folders(self) -> None:
        """Remove empty folders after an update was processed."""
        found = True
        while found:
            found = False
            for directory in self._destination_path.rglob("*"):
                if directory.is_dir():
                    try:
                        directory.rmdir()
                        found = True
                    except (PermissionError, OSError):
                        log.debug("Cannot delete file because locked.")

    def _generate_file_list(self) -> None:
        """Generate the list of files to be copied."""
        log.debug("Generating file list")
        for src_file in self._source_path.rglob("*"):
            if src_file.is_file():
                rel_file_path = src_file.relative_to(self._source_path)
                dst_file = self._destination_path / rel_file_path
                self._file_list.append((src_file, dst_file))
        for src, dst in self._file_list:
            log.debug("generate_file_list Source: %s, Dest: %s", src, dst)

    def _reduce_file_list(self) -> None:
        """Reduce the file list."""
        copy_list = []
        for src, dst in self._file_list:
            log.debug("Comparing %s %s", src, dst)
            try:
                if self._src_files:
                    if self.hash_file(dst) == self._src_files[src]:
                        log.debug("Files are equal")
                        continue
                else:
                    if filecmp.cmp(src, dst, shallow=True):
                        log.debug("Files are equal")
                        continue
            except FileNotFoundError:
                log.debug("File does not exist")
            log.debug("File is to be copied")
            copy_list.append((src, dst))
        log.debug(
            "Finished reduction of copy_list from %s to %s",
            len(self._file_list),
            len(copy_list),
        )
        self._file_list = copy_list

    @staticmethod
    def hash_file(file: Path) -> str:
        """Create a hash for a given file."""
        file_hash = hashlib.sha256()
        with file.open("rb") as fhandle:
            file_block = fhandle.read(65536)
            while len(file_block) > 0:
                file_hash.update(file_block)
                file_block = fhandle.read(65536)
        return file_hash.hexdigest()

    def _parse_json(self) -> None:
        """Parse the update json_file."""
        update_file = self._source_path / "update.json"
        with update_file.open(encoding="utf-8") as f_handle:
            json_obj = json.load(f_handle)
        log.debug("Parsed json: %s", str(json_obj))
        # src_files holds the relative file path and hashes from the json file
        src_files: Dict[str, str] = json_obj["files"]
        for file, hash_ in src_files.items():
            self._src_files[self._source_path / file] = hash_
            src_path = self._source_path / file
            dst_path = self._destination_path / file
            log.debug("Src path: %s, Dest path: %s", src_path, dst_path)
            self._file_list.append((src_path, dst_path))
        self._app_name = json_obj["name"] + ".exe"
        log.debug("App-Name: %s", self._app_name)
