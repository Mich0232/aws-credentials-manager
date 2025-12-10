from base64 import b64decode
from typing import Union

import click

from acm.config import AWS_CREDENTIALS_FILE_PATH
from acm.helpers import read_file_content
from acm.store.utils import (
    alias_exists,
    check_drift_on_current_credentials,
    check_record_for_drift,
    create_record,
    get_current_record,
    get_record_by_alias,
    is_current_record,
    read_store,
    replace_credentials_file,
    update_record,
    write_store,
)


def add_to_store(alias: str, path: str):
    store = read_store()
    if alias_exists(store=store, alias=alias):
        raise click.ClickException(
            f"Alias `{alias}` already exists. Run `acm update {alias} <path>` to update it."
        )

    record = create_record(alias=alias, path=path)
    store.records[alias] = record
    write_store(store=store)


def use_alias(alias: str):
    store = read_store()
    if not alias_exists(store=store, alias=alias):
        raise click.ClickException(f"Alias `{alias}` does not exist.")

    record = get_record_by_alias(store=store, alias=alias)

    if is_current_record(store=store, record=record):
        if check_drift_on_current_credentials(record=record):
            click.echo(
                "Credentials file has drifted. Run `acm update {alias}` to update it."
            )
            return
    else:
        if check_record_for_drift(record=record):
            click.echo(
                "Credentials file has drifted. Run `acm update {alias}` to update it."
            )
            return

    store.current_uuid = record.uuid

    try:
        replace_credentials_file(content=record.content)
    except (PermissionError, FileNotFoundError, OSError, IOError):
        click.echo("Failed to replace credentials file.")
        return

    write_store(store=store)


def list_aliases(wide: bool = False):
    store = read_store()

    for record in store.records.values():
        is_current = "X" if record.uuid == store.current_uuid else " "
        suffix = f"- {record.path}" if wide else ""

        click.echo(f"[{is_current}] - {record.alias} {suffix}")


def show_current_credentials():
    store = read_store()
    current_record = get_current_record(store=store)

    if not current_record:
        click.echo("No credentials file is currently in use.")
        return

    if check_drift_on_current_credentials(record=current_record):
        click.echo(
            "Credentials file has drifted. Run `acm update {alias}` to update it."
        )

    content = b64decode(current_record.content).decode(encoding="utf-8")
    click.echo(content)


def update_alias(alias: str, path: Union[str, None] = None, current: bool = False):
    # TODO: Implement versioning
    store = read_store()
    record = get_record_by_alias(store=store, alias=alias)

    if current:
        content = read_file_content(path=AWS_CREDENTIALS_FILE_PATH)
    elif not path:
        content = read_file_content(path=record.path)
    else:
        content = read_file_content(path=path)

    updated_record = update_record(record=record, content=content)
    store.records[alias] = updated_record
    write_store(store=store)

    click.echo(f"Alias `{alias}` updated using `{path}`.")
