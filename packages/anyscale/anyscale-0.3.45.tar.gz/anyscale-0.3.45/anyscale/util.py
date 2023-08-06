from contextlib import contextmanager
import datetime
import json
import logging
import os
import re
import sys
import threading
import time
from typing import Any, cast, Dict, Iterator, List, Optional, Tuple, Type
import unicodedata
from urllib.parse import quote as quote_sanitize, urlencode as urlencode, urljoin
import webbrowser

import click
import requests
from requests import Response
import yaml

from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.client.openapi_client.rest import ApiException  # type: ignore
import anyscale.conf
from anyscale.credentials import load_credentials

logger = logging.getLogger(__file__)

BOTO_MAX_RETRIES = 5


def confirm(msg: str, yes: bool) -> Any:
    return None if yes else click.confirm(msg, abort=True)


def get_endpoint(endpoint: str, host: Optional[str] = None) -> str:
    return str(urljoin(host or anyscale.conf.ANYSCALE_HOST, endpoint))


def send_json_request_raw(
    endpoint: str,
    json_args: Dict[str, Any],
    method: str = "GET",
    cli_token: Optional[str] = None,
    host: Optional[str] = None,
) -> Response:
    if anyscale.conf.CLI_TOKEN is None and not cli_token:
        anyscale.conf.CLI_TOKEN = load_credentials()

    url = get_endpoint(endpoint, host=host)
    cookies = {"cli_token": cli_token or anyscale.conf.CLI_TOKEN}
    try:
        if method == "GET":
            resp = requests.get(url, params=json_args, cookies=cookies)
        elif method == "POST":
            resp = requests.post(url, json=json_args, cookies=cookies)
        elif method == "DELETE":
            resp = requests.delete(url, json=json_args, cookies=cookies)
        elif method == "PATCH":
            resp = requests.patch(url, data=json_args, cookies=cookies)
        elif method == "PUT":
            resp = requests.put(url, json=json_args, cookies=cookies)
        else:
            assert False, "unknown method {}".format(method)
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Failed to connect to anyscale server at {}".format(url)
        )

    return resp


def send_json_request(
    endpoint: str,
    json_args: Dict[str, Any],
    method: str = "GET",
    cli_token: Optional[str] = None,
    host: Optional[str] = None,
) -> Dict[str, Any]:
    resp = send_json_request_raw(
        endpoint, json_args, method=method, cli_token=cli_token, host=host,
    )

    if not resp.ok:
        if resp.status_code == 500:
            raise click.ClickException(
                "There was an internal error in this command. "
                "Please report this to the Anyscale team at beta@anyscale.com "
                "with the token '{}'.".format(resp.headers["x-trace-id"])
            )

        raise click.ClickException("{}: {}.".format(resp.status_code, resp.text))

    if resp.status_code == 204:
        return {}

    json_resp: Dict[str, Any] = resp.json()
    if "error" in json_resp:
        raise click.ClickException("{}".format(json_resp["error"]))

    return json_resp


# DEPRECATED
def serialize_datetime(d: datetime.datetime) -> str:
    # Make sure that overwriting the tzinfo in the line below is fine.
    # Note that we have to properly convert the timezone if one is
    # already specified. This can be done with the .astimezone method.
    if d.tzinfo is None:
        return d.replace(tzinfo=datetime.timezone.utc).isoformat()
    else:
        return d.astimezone(datetime.timezone.utc).isoformat()


def deserialize_datetime(s: str) -> datetime.datetime:
    if sys.version_info < (3, 7) and ":" == s[-3:-2]:
        s = s[:-3] + s[-2:]

    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f%z")


def humanize_timestamp(timestamp: datetime.datetime) -> str:
    delta = datetime.datetime.now(datetime.timezone.utc) - timestamp
    offset = float(delta.seconds + (delta.days * 60 * 60 * 24))
    delta_s = int(offset % 60)
    offset /= 60
    delta_m = int(offset % 60)
    offset /= 60
    delta_h = int(offset % 24)
    offset /= 24
    delta_d = int(offset)

    if delta_d >= 1:
        return "{} day{} ago".format(delta_d, "s" if delta_d > 1 else "")
    if delta_h > 0:
        return "{} hour{} ago".format(delta_h, "s" if delta_h > 1 else "")
    if delta_m > 0:
        return "{} minute{} ago".format(delta_m, "s" if delta_m > 1 else "")
    else:
        return "{} second{} ago".format(delta_s, "s" if delta_s > 1 else "")


def execution_log_name(session_command_id: str) -> str:
    return "/tmp/ray_command_output_{session_command_id}".format(
        session_command_id=session_command_id
    )


def startup_log_name(session_id: str) -> str:
    return "/tmp/session_startup_logs_{session_id}".format(session_id=session_id)


def slugify(value: str) -> str:
    """
    Code adopted from here https://github.com/django/django/blob/master/django/utils/text.py

    Convert  to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Also strip leading and trailing whitespace.
    """

    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[-\s]+", "-", value)


def get_cluster_config(config_path: str) -> Any:
    with open(config_path) as f:
        cluster_config = yaml.safe_load(f)

    return cluster_config


def get_requirements(requirements_path: str) -> str:
    with open(requirements_path) as f:
        return f.read()


def _resource(name: str, region: str) -> Any:
    import boto3
    from botocore.config import Config

    boto_config = Config(retries={"max_attempts": BOTO_MAX_RETRIES})
    return boto3.resource(name, region, config=boto_config)


def _client(name: str, region: str) -> Any:
    return _resource(name, region).meta.client


def _get_role(role_name: str, region: str) -> Any:
    import botocore

    iam = _resource("iam", region)
    role = iam.Role(role_name)
    try:
        role.load()
        return role
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def _get_user(user_name: str, region: str) -> Any:
    import botocore

    iam = _resource("iam", region)
    user = iam.User(user_name)
    try:
        user.load()
        return user
    except botocore.exceptions.ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "NoSuchEntity":
            return None
        else:
            raise exc


def get_available_regions() -> List[str]:
    import boto3

    client = boto3.client("ec2")
    return [region["RegionName"] for region in client.describe_regions()["Regions"]]


def launch_gcp_cloud_setup(name: str, region: str) -> None:
    # TODO: enforce uniqueness for user's clouds
    quote_safe_name = quote_sanitize(name, safe="")
    query_params = urlencode({"region": region})
    # TODO: Replace this with a proper endpoint
    endpoint = f"/api/v2/clouds/gcp/create/{quote_safe_name}?{query_params}"
    webbrowser.open(get_endpoint(endpoint))


class Timer:
    """
    Code adopted from https://stackoverflow.com/a/39504463/3727678

    Spawn thread and time process that may be blocking.
    """

    def timer_generator(self) -> Iterator[str]:
        while True:
            time_diff = time.gmtime(time.time() - self.start_time)
            yield "{0}: {1}".format(self.message, time.strftime("%M:%S", time_diff))

    def __init__(self, message: str = "") -> None:
        self.message = message
        self.busy = False
        self.start_time = 0.0

    def timer_task(self) -> None:
        while self.busy:
            sys.stdout.write(next(self.timer_generator()))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b" * (len(self.message) + 20))
            sys.stdout.flush()

    def start(self) -> None:
        self.busy = True
        self.start_time = time.time()
        threading.Thread(target=self.timer_task).start()

    def stop(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()
        self.busy = False
        self.start_time = 0.0
        time.sleep(1)


def check_is_feature_flag_on(flag_key: str, default: bool = False) -> bool:
    try:
        use_snapshot_resp = send_json_request(
            "/api/v2/userinfo/check_is_feature_flag_on", {"flag_key": flag_key},
        )
    except Exception:
        return default

    return cast(bool, use_snapshot_resp["result"]["is_on"])


def get_active_sessions(
    project_id: str, session_name: str, api_client: Optional[DefaultApi]
) -> Any:
    if api_client:
        return api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, name=session_name, active_only=True
        ).results
    else:
        response = anyscale.util.send_json_request(
            "/api/v2/sessions/",
            {"project_id": project_id, "name": session_name, "active_only": True},
        )
        return response["results"]


def get_container_name(cluster_config: Dict[str, Any]) -> str:
    return str(cluster_config.get("docker", {}).get("container_name", ""))


def get_autoscaler_container_path(path: str) -> str:
    """
    When autoscaler is run in a separate container, all locations Docker bind-mounted
    from the host to directory /a/b/c of the user container are instead bind-mounted
    to /home/ray/autoscaler_mounts/a/b/c in the autoscaler container.

    Args:
        path: Location in user container.
    Returns:
        Location in the autoscaler container.
    """
    return f"/home/ray/autoscaler_mounts/{path}"


def get_project_directory_name(project_id: str, api_client: DefaultApi = None) -> str:
    # TODO (yiran): return error early if project doesn't exist.
    with format_api_exception(ApiException):
        resp = api_client.get_project_api_v2_projects_project_id_get(project_id)
    directory_name = resp.result.directory_name
    assert len(directory_name) > 0, "Empty directory name found."
    return cast(str, directory_name)


def get_working_dir(
    cluster_config: Dict[str, Any], project_id: str, api_client: DefaultApi = None
) -> str:
    working_dir: Optional[str] = (
        cluster_config.get("metadata", {}).get("anyscale", {}).get("working_dir")
    )
    if working_dir:
        return working_dir
    else:
        return f"/home/ray/{get_project_directory_name(project_id, api_client)}"


def wait_for_session_start(
    project_id: str, session_name: str, api_client: Optional[DefaultApi] = None
) -> str:
    print(f"Waiting for session {session_name} to start.")
    if api_client is None:
        api_client = get_api_client()

    while True:
        sessions = api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, name=session_name, active_only=False
        ).results

        if len(sessions) > 0:
            session = sessions[0]

            if session.state == "Running" and session.pending_state is None:
                return cast(str, session.id)

            # Check for start up errors
            if (
                session.state_data
                and session.state_data.startup
                and session.state_data.startup.startup_error
            ):
                raise click.ClickException(
                    f"Error while starting session {session_name}: {session.state_data.startup.startup_error}"
                )
            elif (
                session.state
                and "Errored" in session.state
                and session.pending_state is None
            ):
                raise click.ClickException(
                    f"Error while starting session {session_name}: Session startup failed due to an error."
                )
            elif (
                session.state
                and session.state in {"Terminated", "Stopped"}
                and session.pending_state is None
            ):
                # Session is created in Terminated state; Check pending state to see if it is pending transition.
                raise click.ClickException(
                    f"Error while starting session {session_name}: Session is still in stopped/terminated state."
                )
        else:
            raise click.ClickException(
                f"Error while starting session {session_name}: Session doesn't exist."
            )

        time.sleep(5)


def wait_for_head_node_start(
    project_id: str,
    session_name: str,
    session_id: str,
    api_client: Optional[DefaultApi] = None,
) -> str:
    url = get_endpoint(f"/projects/{project_id}/sessions/{session_id}")
    print(
        f"Waiting for head node of session {session_name} to start. "
        f"Please view the startup logs at {url}"
    )
    if api_client is None:
        api_client = get_api_client()

    retry_count = 0
    while True:
        sessions = api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, name=session_name, active_only=False
        ).results

        if len(sessions) > 0:
            session = sessions[0]

            if (
                session.state == "Running" and session.pending_state is None
            ) or session.state == "AwaitingFileMounts":
                return cast(str, session.id)

            # Check for start up errors
            if (
                session.state_data
                and session.state_data.startup
                and session.state_data.startup.startup_error
            ):
                raise click.ClickException(
                    f"Error while starting session {session_name}: {session.state_data.startup.startup_error}"
                )
            elif session.state and "Errored" in session.state:
                raise click.ClickException(
                    f"Error while starting session {session_name}: Session startup failed due to an error."
                )
            elif (
                retry_count >= 2
                and session.state
                and session.state in {"Terminated", "Stopped"}
            ):
                # Session is created in Terminated state; Ignore the first few state checks.
                raise click.ClickException(
                    f"Error while starting session {session_name}: Session is still in stopped/terminated state."
                )
        else:
            raise click.ClickException(
                f"Error while starting session {session_name}: Session doesn't exist."
            )

        time.sleep(5)
        retry_count += 1


def download_anyscale_wheel(api_client: DefaultApi, session_id: str) -> None:
    with format_api_exception(ApiException):
        wheel_resp = api_client.session_get_anyscale_wheel_api_v2_sessions_session_id_anyscale_wheel_get(
            session_id=session_id, _preload_content=False
        )
    wheel_path_raw = wheel_resp.headers["content-disposition"]
    assert "filename" in wheel_path_raw, "Error getting anyscale wheel"
    wheel_path = wheel_path_raw.split("filename=")[1].strip('"')
    os.makedirs(os.path.dirname(wheel_path), exist_ok=True)
    with open(wheel_path, "wb+") as f:
        f.write(wheel_resp.data)
        f.flush()


def validate_cluster_configuration(
    cluster_config_file_name: str,
    cluster_config: Optional[DefaultApi] = None,
    api_instance: Optional[DefaultApi] = None,
) -> None:
    assert api_instance

    if not os.path.isfile(cluster_config_file_name):
        raise click.ClickException(
            "The configuration file {} does not exist. Please provide a valid config file.".format(
                cluster_config_file_name
            )
        )

    if not cluster_config:
        try:
            with open(cluster_config_file_name) as f:
                cluster_config = yaml.safe_load(f)
        except (ValueError, yaml.YAMLError):
            raise click.ClickException(
                "\tThe configuration file {} does not have a valid format. "
                "\n\tPlease look at https://github.com/ray-project/ray/blob/master/python/ray/autoscaler/aws/example-full.yaml "
                "for an example configuration file.".format(cluster_config_file_name)
            )

    try:
        api_instance.validate_cluster_api_v2_sessions_validate_cluster_post(
            body={"config": json.dumps(cluster_config)}
        )
    except ApiException as e:
        error = json.loads(json.loads(e.body)["error"]["detail"])
        path = ".".join(error["path"])
        if error["path"]:
            formatted_error = 'Error occured at "{k}: {v}" because {message}.\nSchema description for {k}:\n{schema}'.format(
                k=path,
                v=error["instance"],
                message=error["message"],
                schema=json.dumps(error["schema"], indent=4, sort_keys=True),
            )
        else:
            formatted_error = 'Error occured at "{v}" because {message}.\nSchema description:\n{schema}'.format(
                v=error["instance"],
                message=error["message"],
                schema=json.dumps(error["schema"], indent=4, sort_keys=True),
            )
        raise click.ClickException(
            "The configuration file {0} is not valid.\n{1}".format(
                cluster_config_file_name, formatted_error
            )
        )


def _get_rsync_args(rsync_exclude: List[str], rsync_filter: List[str]) -> List[str]:
    rsync_exclude_args = [["--exclude", exclude] for exclude in rsync_exclude]
    rsync_filter_args = [["--filter", f"dir-merge,- {f}"] for f in rsync_filter]

    # Combine and flatten the two lists
    return [
        arg for sublist in rsync_exclude_args + rsync_filter_args for arg in sublist
    ]


def get_rsync_command(
    ssh_command: List[str],
    source: str,
    ssh_user: str,
    head_ip: str,
    target: str,
    delete: bool,
    rsync_exclude: List[str] = [],
    rsync_filter: List[str] = [],
    dry_run: bool = False,
) -> Tuple[List[str], Optional[Dict[str, Any]]]:
    rsync_executable = "rsync"
    env = None

    command_list = [
        rsync_executable,
        "--rsh",
        " ".join(ssh_command),
        "-avz",
    ]
    command_list += _get_rsync_args(rsync_exclude, rsync_filter)

    if delete:
        # Deletes files in target that doesn't exist in source
        command_list.append("--delete")

    if dry_run:
        command_list += [
            "--dry-run",
            "--itemize-changes",
            "--out-format",
            "%o %f",
        ]

    command_list += [
        source,
        "{}@{}:{}".format(ssh_user, head_ip, target),
    ]
    return command_list, env


def populate_session_args(cluster_config_str: str, config_file_name: str) -> str:
    import jinja2

    env = jinja2.Environment()
    t = env.parse(cluster_config_str)
    for elem in t.body[0].nodes:
        if type(elem) == jinja2.nodes.Getattr:  # type: ignore
            if elem.attr not in os.environ:
                prefixed_command = " ".join(
                    [f"{elem.attr}=<value>", "anyscale"] + sys.argv[1:]
                )
                raise click.ClickException(
                    f"\tThe environment variable {elem.attr} was not set, yet it is required "
                    f"for configuration file {config_file_name}.\n\tPlease specify {elem.attr} "
                    f"by prefixing the command.\n\t\t{prefixed_command}"
                )

    template = jinja2.Template(cluster_config_str)
    cluster_config_filled = template.render(env=os.environ)
    return cluster_config_filled


def canonicalize_remote_location(
    cluster_config: Dict[str, Any], remote_location: Optional[str], project_id: str
) -> Optional[str]:
    """Returns remote_location, but changes it from being based
    in "~/", "/root/" or "/ray" to match working_dir
    """
    # Include the /root path to ensure that absolute paths also work
    # This is because of an implementation detail in OSS Ray's rsync
    if bool(get_container_name(cluster_config)) and bool(remote_location):
        remote_location = str(remote_location)
        working_dir = get_working_dir(cluster_config, project_id)
        for possible_name in ["root", "ray"]:
            full_name = f"/{possible_name}/"
            # TODO(ilr) upstream this to OSS Ray
            if working_dir.startswith("~/") and remote_location.startswith(full_name):
                return remote_location.replace(full_name, "~/", 1)

            if working_dir.startswith(full_name) and remote_location.startswith("~/"):
                return remote_location.replace("~/", full_name, 1)

    return remote_location


@contextmanager
def format_api_exception(exception_type: Type[Exception]) -> Iterator[None]:
    # This should always be called with exceptions that have a status and reason attribute
    try:
        yield
    except exception_type as e:
        if isinstance(e, ApiException):
            raise click.ClickException(f"{e.status}: {str(e)}")

        raise click.ClickException(
            "{0}: {1}".format(e.status, json.loads(e.body)["error"]["detail"])  # type: ignore
        )
