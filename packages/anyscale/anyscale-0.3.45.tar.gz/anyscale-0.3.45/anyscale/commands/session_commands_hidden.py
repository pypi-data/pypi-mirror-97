import datetime
import logging
import os
from typing import Dict, List, Optional

import click

from anyscale.auth_proxy import make_auth_proxy_app
import anyscale.legacy_projects as ray_scripts
from anyscale.project import (
    get_project_id,
    get_project_session,
    load_project_or_throw,
)
from anyscale.snapshot import (
    copy_file,
    get_snapshot_id,
)
from anyscale.util import (
    deserialize_datetime,
    execution_log_name,
    get_endpoint,
    send_json_request,
)


logger = logging.getLogger(__file__)
logging.getLogger("botocore").setLevel(logging.CRITICAL)


@click.group("session", help="Commands for working with sessions.", hidden=True)
def session_cli() -> None:
    pass


@session_cli.command(name="logs", help="Show logs for the current session.")
@click.option("--name", help="Name of the session to run this command on", default=None)
@click.option("--command-id", help="ID of the command to get logs for", default=None)
def session_logs(name: Optional[str], command_id: Optional[int]) -> None:
    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)
    # If the command_id is not specified, determine it by getting the
    # last run command from the active session.
    if not command_id:
        session = get_project_session(project_id, name)
        resp = send_json_request(
            "/api/v2/session_commands/?session_id={}".format(session["id"]), {}
        )
        # Search for latest run command
        last_created_at = datetime.datetime.min
        last_created_at = last_created_at.replace(tzinfo=datetime.timezone.utc)
        for command in resp["results"]:
            created_at = deserialize_datetime(command["created_at"])
            if created_at > last_created_at:
                last_created_at = created_at
                command_id = command["id"]
        if not command_id:
            raise click.ClickException(
                "No comand was run yet on the latest active session {}".format(
                    session["name"]
                )
            )
    resp_out = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "out", "start_line": 0, "end_line": 1000000000},
    )
    resp_err = send_json_request(
        "/api/v2/session_commands/{session_command_id}/execution_logs".format(
            session_command_id=command_id
        ),
        {"log_type": "err", "start_line": 0, "end_line": 1000000000},
    )
    # TODO(pcm): We should have more options here in the future
    # (e.g. show only stdout or stderr, show only the tail, etc).
    print("stdout:")
    print(resp_out["result"]["lines"])
    print("stderr:")
    print(resp_err["result"]["lines"])


# Note: These functions are not normally updated, please cc yiran or ijrsvt on changes.
@session_cli.command(
    name="upload_command_logs", help="Upload logs for a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to upload logs for", type=str, default=None
)
def session_upload_command_logs(command_id: Optional[str],) -> None:
    session_upload_command_logs_impl(command_id)


# session_upload_command_logs_impl is used by:
# - upload_command_logs CLI command
# - web terminal command persister queue
# a separate function is needed to be able to call
# the logic from code rather just CLI.
def session_upload_command_logs_impl(
    command_id: Optional[str],
    cli_token: Optional[str] = None,
    host: Optional[str] = None,
) -> None:
    resp = send_json_request(
        "/api/v2/session_commands/{session_command_id}/upload_logs".format(
            session_command_id=command_id
        ),
        {},
        method="POST",
        cli_token=cli_token,
        host=host,
    )
    assert resp["result"]["session_command_id"] == command_id

    allowed_sources = [
        execution_log_name(command_id) + ".out",
        execution_log_name(command_id) + ".err",
    ]

    for source, target in resp["result"]["locations"].items():
        if source in allowed_sources:
            copy_file(True, source, target, download=False)


# Note: These functions are not normally updated, please cc yiran or ijrsvt on changes.
@session_cli.command(
    name="finish_command", help="Finish executing a command.", hidden=True
)
@click.option(
    "--command-id", help="ID of the command to finish", type=str, required=True
)
@click.option(
    "--stop", help="Stop session after command finishes executing.", is_flag=True
)
@click.option(
    "--terminate",
    help="Terminate session after command finishes executing.",
    is_flag=True,
)
def session_finish_command(command_id: str, stop: bool, terminate: bool) -> None:
    with open(execution_log_name(command_id) + ".status") as f:
        status_code = int(f.read().strip())
    send_json_request(
        f"/api/v2/session_commands/{command_id}/finish",
        {"status_code": status_code, "stop": stop, "terminate": terminate},
        method="POST",
    )


# Note: These functions are not normally updated, please cc yiran or ijrsvt on changes.
@session_cli.command(name="auth_start", help="Start the auth proxy", hidden=True)
@click.option(
    "--auth-token", help="Token for authentication proxy", type=str, required=False
)
def auth_start(auth_token: Optional[str]) -> None:
    from aiohttp import web

    # TODO(pcm): Make this required and pass in after the Docker image is migrated.
    if not auth_token:
        auth_token = os.environ["ANYSCALE_AUTH_TOKEN"]

    assert auth_token, "Auth Token must be set by parameter or environment variable."

    auth_proxy_app = make_auth_proxy_app(auth_token)
    web.run_app(auth_proxy_app)


@session_cli.command(
    name="web_terminal_server", help="Start the web terminal server", hidden=True
)
@click.option(
    "--deploy-environment",
    help="Anyscale deployment type (development, test, staging, production)",
    type=str,
    required=True,
)
@click.option(
    "--use-debugger", help="Activate the Anyscale debugger.", is_flag=True,
)
@click.option(
    "--cli-token",
    help="Anyscale cli token used to instantiate anyscale openapi",
    type=str,
    required=True,
)
@click.option(
    "--host",
    help="Anyscale host used to instantiate anyscale openapi (beta.anyscale.com for example)",
    type=str,
    required=True,
)
@click.option(
    "--working-dir",
    help="The working directory for this anyscale session. The webterminal will be opened from this directory.",
    type=str,
    required=True,
)
@click.option(
    "--session-id", help="The session id of this web terminal", type=str, required=True,
)
def web_terminal_server(
    deploy_environment: str,
    use_debugger: bool,
    cli_token: str,
    host: str,
    working_dir: str,
    session_id: str,
) -> None:
    from anyscale.webterminal.webterminal import main

    main(deploy_environment, use_debugger, cli_token, host, working_dir, session_id)


@click.command(
    name="start",
    context_settings=dict(ignore_unknown_options=True,),
    help="Start a session based on the current project configuration.",
    hidden=True,
)
@click.option("--session-name", help="The name of the created session.", default=None)
# TODO(pcm): Change this to be
# anyscale session start --arg1=1 --arg2=2 command args
# instead of
# anyscale session start --session-args=--arg1=1,--arg2=2 command args
@click.option(
    "--session-args",
    help="Arguments that get substituted into the cluster config "
    "in the format --arg1=1,--arg2=2",
    default="",
)
@click.option(
    "--snapshot",
    help="If set, start the session from the given snapshot.",
    default=None,
)
@click.option(
    "--config",
    help="If set, use this cluster file rather than the default"
    " listed in project.yaml.",
    default=None,
)
@click.option(
    "--min-workers",
    help="Overwrite the minimum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--max-workers",
    help="Overwrite the maximum number of workers in the cluster config.",
    default=None,
)
@click.option(
    "--run", help="Command to run.", default=None,
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--cloud-id", help="Id of the cloud to use", default=None)
@click.option("--cloud-name", help="Name of the cloud to use", default=None)
def anyscale_start(
    session_args: str,
    snapshot: Optional[str],
    session_name: Optional[str],
    config: Optional[str],
    min_workers: Optional[int],
    max_workers: Optional[int],
    run: Optional[str],
    args: List[str],
    cloud_id: Optional[str],
    cloud_name: Optional[str],
) -> None:
    command_name = run

    project_definition = load_project_or_throw()
    project_id = get_project_id(project_definition.root)

    if cloud_id and cloud_name:
        raise click.ClickException("Please provide either cloud id or cloud name.")
    elif cloud_name:
        resp_get_cloud = send_json_request(
            "/api/v2/clouds/find_by_name", {"name": cloud_name}, method="POST"
        )
        cloud = resp_get_cloud["result"]
        cloud_id = cloud["id"]

    if not session_name:
        session_list = send_json_request(
            "/api/v2/sessions/", {"project_id": project_id, "active_only": False}
        )["results"]
        session_name = "session-{0}".format(len(session_list) + 1)

    # Parse the session arguments.
    if config:
        project_definition.config["cluster"]["config"] = config

    session_params: Dict[str, str] = {}

    if command_name:
        command_name = " ".join([command_name] + list(args))
    session_runs = ray_scripts.get_session_runs(session_name, command_name, {})

    assert len(session_runs) == 1, "Running sessions with a wildcard is deprecated"
    session_run = session_runs[0]

    snapshot_id = None
    if snapshot is not None:
        snapshot_id = get_snapshot_id(project_definition.root, snapshot)

    session_name = session_run["name"]
    resp = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name": session_name, "active_only": False},
    )
    if len(resp["results"]) == 0:
        resp = send_json_request(
            "/api/v2/sessions/create_new_session",
            {
                "project_id": project_id,
                "name": session_name,
                "snapshot_id": snapshot_id,
                "session_params": session_params,
                "command_name": command_name,
                "command_params": session_run["params"],
                "shell": True,
                "min_workers": min_workers,
                "max_workers": max_workers,
                "cloud_id": cloud_id,
            },
            method="POST",
        )
    elif len(resp["results"]) == 1:
        if session_params != {}:
            raise click.ClickException(
                "Session parameters are not supported when restarting a session"
            )
        send_json_request(
            "/api/v2/sessions/{session_id}/start".format(
                session_id=resp["results"][0]["id"]
            ),
            {"min_workers": min_workers, "max_workers": max_workers},
            method="POST",
        )
    else:
        raise click.ClickException(
            "Multiple sessions with name {} exist".format(session_name)
        )
    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Session {session_name} starting. View progress at {url}")
