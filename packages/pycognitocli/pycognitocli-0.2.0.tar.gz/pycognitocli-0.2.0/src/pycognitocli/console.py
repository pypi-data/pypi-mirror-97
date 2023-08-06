"""CLI entrypoints for pycognitocli"""
from typing import Any
import logging

import click
from libadvian.logging import init_logging
from pycognito import Cognito  # type: ignore

from pycognitocli import __version__

# pylint: disable=R0913
LOGGER = logging.getLogger(__name__)


@click.group()
@click.version_option(version=__version__)
@click.option("-l", "--loglevel", help="Python log level, 10=DEBUG, 20=INFO, 30=WARNING, 40=CRITICAL", default=30)
@click.option("-v", "--verbose", count=True, help="Shorthand for info/debug loglevel (-v/-vv)")
@click.option(
    "-p",
    "--poolid",
    required=True,
    envvar="COGNITO_POOL_ID",
    help="Pool id (defaults to COGNITO_POOL_ID env)",
)
@click.option(
    "-a",
    "--appid",
    required=True,
    envvar="COGNITO_APP_ID",
    help="App id (defaults to COGNITO_APP_ID env)",
)
@click.option(
    "-cs",
    "--clientsecret",
    envvar="COGNITO_APP_SECRET",
    help="App client secret (defaults to COGNITO_APP_SECRET env)",
)
@click.pass_context
def cligroup(ctx: Any, loglevel: int, verbose: int, poolid: str, appid: str, clientsecret: str) -> None:
    """CLI wrapper select operations in pycognito"""
    if verbose == 1:
        loglevel = 20
    if verbose >= 2:
        loglevel = 10
    logging.getLogger("").setLevel(loglevel)
    LOGGER.setLevel(loglevel)
    ctx.ensure_object(dict)
    ctx.obj["poolid"] = poolid
    ctx.obj["appid"] = appid
    ctx.obj["client"] = Cognito(poolid, appid)
    if clientsecret:
        ctx.obj["client"].client_secret = clientsecret


@cligroup.group()
@click.pass_context
def token(ctx: Any) -> None:
    """Token commands"""
    _ = ctx


@token.command()
@click.option(
    "-u",
    "--username",
    prompt=True,
    envvar="COGNITO_USERNAME",
    help="Username (defaults to COGNITO_USERNAME env)",
)
@click.option(
    "-pw",
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    envvar="COGNITO_PASSWORD",
    help="Password(defaults to COGNITO_PASSWORD env)",
)
@click.option("-c", "--curl", is_flag=True, help="Output authorization header for curl")
@click.pass_context
def get(ctx: Any, username: str, password: str, curl: bool) -> None:
    """Get auth token"""
    client = ctx.obj["client"]
    client.username = username
    client.authenticate(password)
    if curl:
        click.echo(f"-H 'Authorization: {client.token_type} {client.id_token}'")
        return
    click.echo(f"{client.token_type} {client.id_token}")


def pycognitocli_cli() -> None:
    """CLI wrapper select operations in pycognito"""
    init_logging(logging.WARNING)
    LOGGER.setLevel(logging.WARNING)
    cligroup()  # pylint: disable=E1120
