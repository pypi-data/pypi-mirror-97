import click
from click.utils import echo

from .db import init_db
from . import aes

@click.group()
def cli():
    pass

@click.command("encrypt")
@click.argument("message")
@click.password_option(type=str, confirmation_prompt=True)
def encrypt(message, password):
    a = aes.encrypt(message, password)
    click.echo(a)

@click.command("decrypt")
@click.argument("message")
@click.password_option(type=str, confirmation_prompt=False)
def decrypt(message, password):
    a = aes.decrypt(message, password)
    click.echo(a)


cli.add_command(encrypt)
cli.add_command(decrypt)