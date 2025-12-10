import click

from acm.store.helpers import (
    add_to_store,
    list_aliases,
    show_current_credentials,
    update_alias,
    use_alias,
)
from acm.store.utils import init_store


@click.group()
def cli():
    pass


@cli.command("add")
@click.argument("path", type=click.Path())
@click.argument("alias", type=str)
def add(path, alias: str):
    add_to_store(alias=alias, path=path)

    click.echo(f"File stored successfully under '{alias}' alias.")


@cli.command("list")
@click.option(
    "-o", "--output", type=click.Choice(["default", "wide"]), default="default"
)
def list(output: str = "default"):
    wide = output == "wide"
    list_aliases(wide=wide)


@cli.command("use")
@click.argument("alias", type=str)
def use(alias: str):
    use_alias(alias=alias)

    click.echo(f"Now using: {alias}")


@cli.command("update")
@click.argument("alias", type=str)
@click.argument("path", type=click.Path(), required=False)
@click.option("--current", is_flag=False, flag_value="True", default=None)
def update(alias: str, path: str = None, current: bool = False):
    if path and current:
        raise click.ClickException(
            "Both `path` and `--current` flags cannot be provided."
        )

    update_alias(alias=alias, path=path, current=current)


@cli.command("init")
def init():
    init_store()


@cli.command("show")
def show():
    show_current_credentials()
