import click

from acm.store.utils import (
    alias_exists,
    create_record,
    get_record_by_alias,
    read_store,
    write_store,
)


def add_to_store(alias: str, path: str):
    store = read_store()
    if alias_exists(store=store, alias=alias):
        raise click.ClickException(
            f"Alias `{alias}` already exists. Run `acm update {alias} <path>` to update it."
        )

    record = create_record(alias=alias, path=path)
    store.records.append(record)
    write_store(store=store)


def use_alias(alias: str):
    store = read_store()
    if not alias_exists(store=store, alias=alias):
        raise click.ClickException(f"Alias `{alias}` does not exist.")

    record = get_record_by_alias(store=store, alias=alias)
    store.current_uuid = record.uuid
    write_store(store=store)


def list_aliases():
    store = read_store()

    for record in store.records:
        if record.uuid == store.current_uuid:
            click.echo(f"[X] - {record.alias}")
        else:
            click.echo(f"[ ] - {record.alias}")
