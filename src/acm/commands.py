import hashlib

import click

from acm.helpers import (
    get_currently_used_alias,
    init,
    read_store,
    set_currently_used_alias,
    store_credentials_file,
    use_credentials_file,
    write_store,
)
from acm.store.helpers import add_to_store, list_aliases, show_current_credentials


@click.group()
def cli():
    pass


@click.command("init")
def initialize():
    init()


@click.command("add")
@click.argument("path", type=click.Path())
@click.argument("alias", type=str)
def add_file(path, alias: str):
    with open(path, "rb") as file:
        content = file.read()
        hex_digest = str(hashlib.md5(content).hexdigest())

        store_credentials_file(file_hash=hex_digest, content=content)
        write_store(**{f"alias-{alias}": hex_digest})

    click.echo("File stored successfully")


@click.command("list")
def list_elements():
    elements = read_store()
    current_alias = get_currently_used_alias()

    for k, v in elements.items():
        if k.startswith("alias-"):
            alias = k.replace("alias-", "")
            if alias == current_alias:
                click.secho(f"[X] {alias}")
            else:
                click.echo(f"[ ] {alias}")


@click.command()
@click.argument("alias", type=str)
def remove_file(alias):
    elements = read_store()
    for k, v in elements.items():
        if k == f"alias-{alias}":
            # TODO: Ability to remove from store
            pass


@click.command("use")
@click.argument("alias", type=str)
def use_alias(alias):
    elements = read_store()
    hash = None
    for k, v in elements.items():
        if k == f"alias-{alias}":
            hash = v
            break

    use_credentials_file(file_hash=hash)
    set_currently_used_alias(alias=alias)
    click.echo(f"Now using: {alias}")


@click.group("v2")
def v2():
    pass


@v2.command("add")
@click.argument("path", type=click.Path())
@click.argument("alias", type=str)
def add_file_v2(path, alias: str):
    add_to_store(alias=alias, path=path)

    click.echo(f"File stored successfully under '{alias}' alias.")


@v2.command("list")
def list_v2():
    list_aliases()


@v2.command("use")
@click.argument("alias", type=str)
def use_alias_v2(alias: str):
    from acm.store.helpers import use_alias

    use_alias(alias=alias)

    click.echo(f"Now using: {alias}")


@v2.command("init")
def init_v2():
    from acm.store.utils import init_store

    init_store()


@v2.command("show")
def show_v2():
    show_current_credentials()


cli.add_command(initialize)
cli.add_command(add_file)
cli.add_command(list_elements)
cli.add_command(use_alias)
cli.add_command(v2)
