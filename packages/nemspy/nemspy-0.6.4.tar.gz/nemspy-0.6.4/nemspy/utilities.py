from datetime import datetime
import logging
import os
from os import PathLike
from pathlib import Path
import shutil
import sys
from typing import Union


def repository_root(path: PathLike = None) -> str:
    if path is None:
        path = __file__
    if not isinstance(path, Path):
        path = Path(path)
    if path.is_file():
        path = path.parent
    if '.git' in (child.name for child in path.iterdir()) or path == path.parent:
        return path
    else:
        return repository_root(path.parent)


def get_logger(
    name: str,
    log_filename: PathLike = None,
    file_level: int = None,
    console_level: int = None,
    log_format: str = None,
) -> logging.Logger:
    if file_level is None:
        file_level = logging.DEBUG
    if console_level is None:
        console_level = logging.INFO
    logger = logging.getLogger(name)

    # check if logger is already configured
    if logger.level == logging.NOTSET and len(logger.handlers) == 0:
        # check if logger has a parent
        if '.' in name:
            logger.parent = get_logger(name.rsplit('.', 1)[0])
        else:
            # otherwise create a new split-console logger
            logger.setLevel(logging.DEBUG)
            if console_level != logging.NOTSET:
                if console_level <= logging.INFO:
                    class LoggingOutputFilter(logging.Filter):
                        def filter(self, rec):
                            return rec.levelno in (logging.DEBUG, logging.INFO)

                    console_output = logging.StreamHandler(sys.stdout)
                    console_output.setLevel(console_level)
                    console_output.addFilter(LoggingOutputFilter())
                    logger.addHandler(console_output)

                console_errors = logging.StreamHandler(sys.stderr)
                console_errors.setLevel(max((console_level, logging.WARNING)))
                logger.addHandler(console_errors)

    if log_filename is not None:
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(file_level)
        for existing_file_handler in [
            handler for handler in logger.handlers if type(handler) is logging.FileHandler
        ]:
            logger.removeHandler(existing_file_handler)
        logger.addHandler(file_handler)

    if log_format is None:
        log_format = '[%(asctime)s] %(name)-13s %(levelname)-8s: %(message)s'
    log_formatter = logging.Formatter(log_format)
    for handler in logger.handlers:
        handler.setFormatter(log_formatter)

    return logger


LOGGER = get_logger('utilities')


def create_symlink(from_filename: PathLike, to_filename: PathLike, overwrite: bool = False):
    if not isinstance(from_filename, Path):
        from_filename = Path(from_filename)
    if not isinstance(to_filename, Path):
        to_filename = Path(to_filename)

    if to_filename.exists() and overwrite:
        os.remove(to_filename)

    try:
        to_filename.symlink_to(from_filename)
    except Exception as error:
        LOGGER.warning(f'could not create symbolic link: {error}')
        shutil.copyfile(from_filename, to_filename)


def parse_datetime(value: Union[int, float, str, datetime]):
    if not isinstance(value, datetime):
        if isinstance(value, int) or isinstance(value, float):
            value = datetime.fromtimestamp(value)
        elif isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            raise TypeError(
                f'unable to convert value of type "{type(value)}" to datetime: {value}'
            )
    return value
