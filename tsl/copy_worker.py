"""Definition for CopyWorker to Update TSL apps."""
import filecmp
import hashlib
import json
import logging
import ntpath
import os
import shutil
import time
from typing import Dict, List, Tuple

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QEventLoop, QTimer

log = logging.getLogger("tsl.copy_worker")  # pylint: disable=invalid-name


class CopyWorker(QObject):
    """Worker object processing an update."""

    current_file = pyqtSignal(str, name="current_file")
    files_copied = pyqtSignal(int, int, name="files_copied")
    copy_finished = pyqtSignal(name="copy_finished")
    status_changed = pyqtSignal(str, name="status_changed")

    def __init__(self, path: str, file: str, parent: QObject = None) -> None:
        """
        Create a new CopyWorker.

        The given path is the path into which the application will be
        installed.

        The file is the former txt file. You can use any path you want as we
        will look for the update.json anyway.
        """
        super(CopyWorker, self).__init__(parent)
        self._path = path
        self._exe_path = ""
        self._source = ntpath.split(file)[0]
        self._app_name = ""
        self._hashes: Dict[str, str]
        log.debug("Path: %s", self._path)
        log.debug("Source: %s", self._source)

        self._file_list: List[Tuple[str, str]] = []

    @property
    def exe_path(self) -> str:
        """Return the executable path of the app."""
        return os.path.join(self._path, self._app_name)

    @pyqtSlot(name="start_copy")
    def start_copy(self) -> None:
        """Start to copy the files from the def file to the destination."""
        self.status_changed.emit("Checking TSL definition file of update.")
        log.debug("Checking file: %s",
                  os.path.join(self._source, "update.json"))
        if os.path.exists(os.path.join(self._source, "update.json")):
            self.status_changed.emit("Reading TSL definition file.")
            self._parse_json()
        else:
            self.status_changed.emit("update_failed")
            return
        self.status_changed.emit("Removing obsolete files from "
                                 "installation folder.")
        self._remove_files()
        self._remove_empty_folders()
        self.status_changed.emit("Calculating list of files to be copied")
        self._reduce_file_list()
        self.status_changed.emit("Copying files...")

        for idx, file in enumerate(self._file_list):
            src, dst = file
            self.current_file.emit(dst)
            log.debug("Coping from %s to %s", src, dst)
            try:
                folder = ntpath.split(dst)[0]
                log.debug("Trying to create folder %s", folder)
                os.makedirs(folder)
            except FileExistsError:
                log.debug("Folder does already exist")
            try_count = 30
            while try_count:
                try:
                    self.copy_file(dst, src)
                    break
                except PermissionError:
                    log.warning("Received permission error copying file to %s",
                                dst)
                    try_count -= 1
                    time.sleep(5)
            else:
                log.debug("The updated failed")
                self.status_changed.emit("Update failed.")
            self.files_copied.emit(idx + 1, len(self._file_list))
        self.files_copied.emit(100, 100)
        self.copy_finished.emit()
        self.status_changed.emit("Update complete.")

    @staticmethod
    def copy_file(dst: str, src: str) -> None:
        """Copy a file from dst to src."""
        count = 30
        while count > 0:
            try:
                shutil.copy(src, dst)
                count = 0
            except PermissionError:
                log.warning("Could not copy to  %s due to PermissionError",
                            dst)
                # sleep 1 second in an event loop
                loop = QEventLoop()
                QTimer.singleShot(1000, loop.quit)
                loop.exec()
                count -= 1

    def _remove_files(self) -> None:
        """Remove files from the path that aren't needed anymore."""
        log.debug("Deleting obsolete files")
        for root, _, files in os.walk(self._path):
            for file in files:
                full_path = os.path.join(root, file)
                if not any(full_path == dst_path
                           for _, dst_path in self._file_list):
                    log.debug("Removing file %s", file)
                    try:
                        os.remove(full_path)
                    except PermissionError:
                        log.debug("Cannot delete file because locked.")
        log.debug("Deletion of obsolete files finished")

    def _remove_empty_folders(self) -> None:
        """Remove empty folders after an update was processed."""
        found = True
        while found:
            found = False
            for root, dirs, _ in os.walk(self._path):
                for folder in dirs:
                    if not os.listdir(os.path.join(root, folder)):
                        log.debug("Removing folder %s", folder)
                        found = True
                        try:
                            shutil.rmtree(os.path.join(root, folder))
                        except PermissionError:
                            log.debug("Cannot delete file because locked.")

    def _generate_file_list(self) -> None:
        """Generate the list of files to be copied."""
        log.debug("Generating file list")
        for root, _, files in os.walk(self._source):
            log.debug(files)
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = src_path.replace(self._source, self._path)
                self._file_list.append((src_path, dst_path))

        log.debug("Finished generating file list: %s", str(self._file_list))
        for src, dst in self._file_list:
            log.debug("Source %s; Dest. %s", src, dst)

    def _reduce_file_list(self) -> None:
        """Reduce the file list."""
        copy_list = []
        for src, dst in self._file_list:
            log.debug("Comparing")
            log.debug(src)
            log.debug(dst)
            try:
                if self._hashes:
                    if self.hash_file(dst) == \
                            self._hashes[dst.replace(self._path + "\\", "")]:
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
        log.debug("Finished reduction of copy_list from %s to %s",
                  len(self._file_list), len(copy_list))
        self._file_list = copy_list

    @staticmethod
    def hash_file(file: str) -> str:
        """Create a hash for a given file."""
        file_hash = hashlib.sha256()
        with open(file, 'rb') as fhandle:
            file_block = fhandle.read(65536)
            while len(file_block) > 0:
                file_hash.update(file_block)
                file_block = fhandle.read(65536)
        return file_hash.hexdigest()

    def _parse_json(self) -> None:
        """Parse the update json_file."""
        with open(os.path.join(self._source, "update.json")) as fhandle:
            json_obj = json.load(fhandle)
        log.debug("Parsed json: %s", str(json_obj))
        for file in json_obj["files"]:
            src_path = os.path.join(self._source, file)
            dst_path = src_path.replace(self._source, self._path)
            log.debug("Adding src: %s", src_path)
            log.debug("Destination: %s", dst_path)
            self._file_list.append((src_path, dst_path))
        self._hashes = json_obj["files"]
        self._app_name = json_obj["name"] + ".exe"
        log.debug("App-Name: %s", self._app_name)
