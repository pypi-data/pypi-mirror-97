import logging
import os
import shutil
import stat
from pathlib import Path

_logger = logging.getLogger(__name__)


def copy_children(source_dir: Path,
                  target_dir: Path,
                  merge_directories: bool = True,
                  overwrite_files: bool = False):
    """Low performance function for copying tree"""
    if not target_dir.exists():
        raise Exception(f"The target directory '{target_dir}' does not exist.")
    for child in source_dir.iterdir():
        target_path_for_child = target_dir.joinpath(child.name)
        if child.is_dir():
            if not merge_directories and target_path_for_child.exists():
                raise Exception(f"The directory (or possibly file) '{target_path_for_child}' does already exist.")
            _logger.debug(f"Copying directory {child} to {target_path_for_child}")
            target_path_for_child.mkdir(exist_ok=True)
            copy_children(child, target_path_for_child,
                          merge_directories=merge_directories,
                          overwrite_files=overwrite_files)
            # shutil.copytree(child, target_path_for_child, ) # not used because not configurable enough
        else:
            if target_path_for_child.exists():
                if not overwrite_files:
                    raise Exception(f"The file (or possibly directory) '{target_path_for_child}' does already exist. "
                                    f"It would be overwritten by {child}")
                else:
                    _logger.debug(f"Deleting {target_path_for_child} to overwrite it with {child}")
                    target_path_for_child.unlink()
            _logger.debug(f"Copying file {child} to {target_path_for_child}")
            shutil.copyfile(str(child), str(target_path_for_child))


def assert_path_exists(path: Path):
    if not path.exists():
        raise Exception(f"The path {str(path)} does not exist")


def assert_path_is_file(path: Path):
    if not path.is_file():
        raise Exception(f"The path {str(path)} does not exist or is no file")


def make_file_executable_if_necessary(file: Path):
    assert_path_is_file(file)
    if not os.access(str(file), os.X_OK):
        mode = file.stat().st_mode
        new_mode = mode | stat.S_IEXEC
        _logger.info(f"Making file {file} executable")
        file.chmod(new_mode)
