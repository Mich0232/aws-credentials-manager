import hashlib
from typing import Union


def read_file_content(path: str) -> bytes:
    with open(path, "rb") as file:
        return file.read()


def get_content_hash(content: Union[str, bytes]) -> str:
    return str(hashlib.md5(content).hexdigest())
