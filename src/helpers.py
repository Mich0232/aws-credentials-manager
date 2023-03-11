import shutil
from pathlib import Path
from typing import Dict

from src.exceptions import AWSProfileManagerException


def init():
    try:
        config_dir_path = Path.home() / ".apm"
        config_dir_path.mkdir()

        store_file_path = config_dir_path / "store"
        store_file_path.touch()
    except FileExistsError:
        raise AWSProfileManagerException(
            "APM configuration already exists under ~/.apm"
        )


def read_store() -> Dict[str, str]:
    store_path = Path.home() / ".apm/store"

    with open(store_path, "r") as store_file:
        config_lines = store_file.readlines()
        config = []
        for line in config_lines:
            line = line.strip("\n")
            config.append(tuple(line.split("=")))
        return dict(config)


def write_store(**config):
    store_path = Path.home() / ".apm/store"

    with open(store_path, "a") as store_file:
        store_file.writelines([f"{k}={v}\n" for k, v in config.items()])


def store_credentials_file(file_hash: str, content: bytes):
    config_dir_path = Path.home() / ".apm"

    _filename = f"{file_hash}.stored"
    with open(config_dir_path / _filename, "wb") as new_file:
        new_file.write(content)


def use_credentials_file(file_hash: str):
    current_credentials_path = Path.home() / ".aws/credentials"
    shutil.copy(current_credentials_path, Path.home() / ".apm/previous")
    shutil.copy(Path.home() / f".apm/{file_hash}.stored", current_credentials_path)
