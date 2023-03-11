import hashlib

from lib import click
from src.helpers import (
    init,
    read_store,
    store_credentials_file,
    use_credentials_file,
    write_store,
)


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
    for k, v in elements.items():
        if k.startswith("alias-"):
            click.echo(k.replace("alias-", ""))


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
    click.echo(f"Now using: {alias}")


cli.add_command(initialize)
cli.add_command(add_file)
cli.add_command(list_elements)
cli.add_command(use_alias)
