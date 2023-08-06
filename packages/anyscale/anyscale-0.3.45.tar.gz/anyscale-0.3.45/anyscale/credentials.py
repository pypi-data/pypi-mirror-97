import json
import os
from typing import Dict

import click

import anyscale


def load_credentials() -> str:
    # The environment variable ANYSCALE_CLI_TOKEN can be used to
    # overwrite the credentials in ~/.anyscale/credentials.json
    if "ANYSCALE_CLI_TOKEN" in os.environ:
        return os.environ["ANYSCALE_CLI_TOKEN"]
    path = os.path.expanduser("~/.anyscale/credentials.json")
    if not os.path.exists(path):
        raise click.ClickException(
            "Credentials not found. You need to create an account at {0} "
            "and then go to {0}/credentials and follow the instructions.".format(
                anyscale.conf.ANYSCALE_HOST
            )
        )
    with open(path) as f:
        try:
            credentials: Dict[str, str] = json.load(f)
        except json.JSONDecodeError:
            msg = (
                "Unable to load user credentials.\n\nTip: Try creating your "
                "user credentials again by going to {}/credentials and "
                "following the instructions. If this does not work, "
                "please contact Anyscale support!".format(anyscale.conf.ANYSCALE_HOST)
            )
            raise click.ClickException(msg)
    if "cli_token" not in credentials:
        raise click.ClickException("Credential file not valid, please regenerate it.")
    return credentials["cli_token"]
