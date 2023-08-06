import os
import click
from tabulate import tabulate
from demyst.common.config import load_config

@click.group()
def auth():
    pass

@auth.command()
@click.option('--env', default="prod", required=False, help='Environment (stg or prod).')
def sign_in(env):
    config = load_config(config_file=None, username=None, password=None, key=None, env=env, region=None)
    token_is_valid = config.jwt_token_is_valid()
    if token_is_valid:
        fullname = config.get_console_fullname()
        email = config.get_username()
        click.echo("Already signed in with the following account")
        click.echo("Email: {}".format(email))
        click.echo("Name: {}".format(fullname))
    else:
        config.prompt_for_jwt_token_and_cache_it()
        fullname = config.get_console_fullname()
        email = config.get_username()
        click.echo("Successfully signed in with the following account")
        click.echo("Email: {}".format(email))
        click.echo("Name: {}".format(fullname))


@auth.command()
def sign_out():
    config = load_config(config_file=None, username=None, password=None, key=None, env=None, region=None)
    config.remove_jwt_token()
    click.echo("Successfully Signed Out")