import logging
import shutil
import tempfile
from pathlib import Path

_logger = logging.getLogger(__name__)


def create_temp_dir(preferred_name: str) -> Path:
    system_temp_dir = Path(tempfile.gettempdir())
    temp_dir = system_temp_dir.joinpath(preferred_name)
    if temp_dir.exists():
        temp_dir = Path(tempfile.mkdtemp(prefix=preferred_name))
    else:
        temp_dir.mkdir(exist_ok=False)
    return temp_dir


def create_temp_file(preferred_name: str) -> Path:
    system_temp_dir = Path(tempfile.gettempdir())
    temp_file = system_temp_dir.joinpath(preferred_name)
    if temp_file.exists():
        temporary_file_fd, temporary_file_name = tempfile.mkstemp(prefix=preferred_name)
        temp_file = Path(temporary_file_name)
    else:
        temp_file.touch(exist_ok=False)
    return temp_file


class CreateTempFileFor:
    def __init__(self,
                 file: Path,
                 cleanup: bool = True):
        self._file = file
        self._cleanup = cleanup

    def __enter__(self) -> Path:
        preferred_temp_file_name = self._file.name
        self._temp_file = create_temp_file(preferred_temp_file_name)
        if not self._file.exists():
            raise Exception(f"file {self._file} does not exist")
        self._temp_file.write_bytes(self._file.read_bytes())
        logging.info(f"{CreateTempFileFor.__name__}: Created temp file {str(self._temp_file)}")
        return self._temp_file

    def __exit__(self, exc_type, exc_value, traceback):
        if self._cleanup:
            logging.info(f"{CreateTempFileFor.__name__}: Removing temp file {str(self._temp_file)}")
            self._temp_file.unlink()


class CreateTempFile:
    def __init__(self,
                 preferred_name: str,
                 cleanup: bool = True):
        self._preferred_name = preferred_name
        self._cleanup = cleanup

    def __enter__(self) -> Path:
        self._temp_file = create_temp_file(self._preferred_name)
        logging.info(f"{CreateTempFileFor.__name__}: Created temp file {str(self._temp_file)}")
        return self._temp_file

    def __exit__(self, exc_type, exc_value, traceback):
        if self._cleanup:
            if self._temp_file.exists():
                logging.info(f"{CreateTempFileFor.__name__}: Removing temp file {str(self._temp_file)}")
                self._temp_file.unlink()


class CreateTempDirectory:
    def __init__(self,
                 preferred_name: str,
                 cleanup: bool = True):
        self._preferred_name = preferred_name
        self._cleanup = cleanup

    def __enter__(self) -> Path:
        self._temp_dir = create_temp_dir(self._preferred_name)
        logging.info(f"{CreateTempDirectory.__name__}: Created temp directory {str(self._temp_dir)}")
        return self._temp_dir

    def __exit__(self, exc_type, exc_value, traceback):
        if self._cleanup:
            if self._temp_dir.exists():
                logging.info(f"{CreateTempDirectory.__name__}: Removing temp directory {str(self._temp_dir)}")
                shutil.rmtree(self._temp_dir)
