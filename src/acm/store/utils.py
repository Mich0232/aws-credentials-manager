import shutil
import uuid
from base64 import b64decode, b64encode
from datetime import datetime
from typing import Union

import click
from pydantic import ValidationError

from acm.config import (
    AWS_CREDENTIALS_FILE_PATH,
    BACKUP_FILE_PATH,
    CONFIG_ROOT_PATH,
    STORE_FILE_PATH,
)
from acm.files import get_content_hash, read_file_content
from acm.store.models import Record, Store


def serialize_store(store: Store):
    return store.model_dump_json()


def deserialize_store(json_string: str) -> Store:
    return Store.model_validate_json(json_string)


def read_store() -> Store:
    try:
        with open(STORE_FILE_PATH, "r") as store_file:
            return deserialize_store(store_file.read())
    except (FileNotFoundError, ValidationError):
        raise click.ClickException(
            "Store not initialized. Run `acm v2 init` to initialize store."
        )


def write_store(store: Store, update_version: bool = True):
    if update_version:
        store.version = int(datetime.now().timestamp())

    with open(STORE_FILE_PATH, "w+") as store_file:
        store_file.write(serialize_store(store))


def create_record(alias: str, path: str) -> Record:
    content = read_file_content(path)
    hex_digest = get_content_hash(content)
    timestamp = int(datetime.now().timestamp())
    _id = uuid.uuid4().hex

    return Record(
        uuid=_id,
        alias=alias,
        path=path,
        content=b64encode(content),
        hash=hex_digest,
        created_at=timestamp,
        updated_at=timestamp,
    )


def update_record(record: Record, content: bytes) -> Record:
    record.content = b64encode(content)
    record.hash = get_content_hash(content)
    record.updated_at = int(datetime.now().timestamp())
    return record


def get_record_by_alias(store: Store, alias: str) -> Union[Record, None]:
    return store.records.get(alias, None)


def get_current_record(store: Store) -> Union[Record, None]:
    current_uuid = store.current_uuid
    if not current_uuid:
        return None

    for record in store.records.values():
        if record.uuid == current_uuid:
            return record


def is_current_record(store: Store, record: Record) -> bool:
    return store.current_uuid == record.uuid


def alias_exists(store: Store, alias: str) -> bool:
    return alias in store.records.keys()


def init_store():
    CONFIG_ROOT_PATH.mkdir(parents=True, exist_ok=True)

    if STORE_FILE_PATH.exists():
        click.echo("Store file already exists. Skipping initialization.")
        return
    else:
        write_store(Store(records={}, version=0, current_uuid=""))

    click.echo("Store initialized successfully.")


def replace_credentials_file(content: bytes, backup: bool = True):
    if backup:
        shutil.copy(AWS_CREDENTIALS_FILE_PATH, BACKUP_FILE_PATH)

    with open(AWS_CREDENTIALS_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(b64decode(content).decode(encoding="utf-8"))


def check_drift_on_current_credentials(record: Record) -> bool:
    current_content = read_file_content(AWS_CREDENTIALS_FILE_PATH)
    if b64encode(current_content) != record.content:
        return True
    return False


def check_record_for_drift(record: Record) -> bool:
    current_content = read_file_content(record.path)
    if b64encode(current_content) != record.content:
        return True
    return False
