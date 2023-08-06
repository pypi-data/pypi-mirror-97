import json
import os
import shutil
import sys
from typing import Any, Dict, Optional, Tuple

import click
from click import ClickException
import jsonschema
from openapi_client.rest import ApiException  # type: ignore
import yaml

import anyscale
from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.util import (
    format_api_exception,
    get_endpoint,
    send_json_request,
    slugify,
    validate_cluster_configuration,
)

ANYSCALE_PROJECT_FILE = ".anyscale.yaml"
ANYSCALE_AUTOSCALER_FILE = "session-default.yaml"


CLUSTER_YAML_TEMPLATE = open(
    os.path.join(os.path.dirname(__file__), "default_anyscale_aws.yaml")
).read()

CLUSTER_CONFIG_TEMPLATE_STR = json.dumps(
    yaml.load(CLUSTER_YAML_TEMPLATE, Loader=yaml.SafeLoader)
)


def validate_project_schema(project_config: Dict[str, str]) -> Any:
    """Validate a project config against the project schema.
    Args:
        project_config (dict): Parsed project yaml.
    Raises:
        jsonschema.exceptions.ValidationError: This exception is raised
            if the project file is not valid.
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir, "ProjectConfig.json")) as f:
        schema = json.load(f)

    jsonschema.validate(instance=project_config, schema=schema)


def find_project_root(directory: str) -> Optional[str]:
    """Find root directory of the project.

    Args:
        directory (str): Directory to start the search in.

    Returns:
        Path of the parent directory containing the project
        or None if no such project is found.
    """
    prev, directory = None, os.path.abspath(directory)
    while prev != directory:
        if os.path.exists(os.path.join(directory, ANYSCALE_PROJECT_FILE)):
            return directory
        prev, directory = directory, os.path.abspath(os.path.join(directory, os.pardir))
    return None


class ProjectDefinition(object):
    def __init__(self, root_dir: str):
        self.root = os.path.join(root_dir, "")
        anyscale_yaml = os.path.join(root_dir, ANYSCALE_PROJECT_FILE)
        if os.path.exists(anyscale_yaml):
            with open(anyscale_yaml) as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {}

        if "cluster" not in self.config:
            self.config["cluster"] = {
                "config": os.path.join(self.root, ANYSCALE_AUTOSCALER_FILE)
            }

    def cluster_yaml(self) -> str:
        if "config" in self.config["cluster"]:
            return str(self.config["cluster"]["config"])
        return os.path.join(self.root, ANYSCALE_AUTOSCALER_FILE)


def load_project_or_throw() -> ProjectDefinition:
    # First check if there is a .anyscale.yaml.
    root_dir = find_project_root(os.getcwd())
    if not root_dir:
        raise ClickException("No project directory found")
    return ProjectDefinition(root_dir)


def get_project_id(project_dir: str) -> str:
    """
    Args:
        project_dir: Project root directory.

    Returns:
        The ID of the associated Project in the database.

    Raises:
        ValueError: If the current project directory does
            not contain a project ID.
    """
    project_filename = os.path.join(project_dir, ANYSCALE_PROJECT_FILE)
    if os.path.isfile(project_filename):
        with open(project_filename) as f:
            config = yaml.safe_load(f)
            project_id = config["project_id"]
    else:
        # TODO(pcm): Consider doing this for the user and retrying the command
        # they were trying to run.
        raise ClickException(
            "Ray project in {} not registered yet. "
            "Did you run 'anyscale init'?".format(project_dir)
        )
    try:
        result = str(project_id)
    except ValueError:
        # TODO(pcm): Tell the user what to do here.
        raise ClickException(
            "{} does not contain a valid project ID".format(project_filename)
        )
    return result


def validate_project_name(project_name: str) -> bool:
    return " " not in project_name.strip()


def get_project_sessions(
    project_id: str, session_name: Optional[str], api_client: DefaultApi = None
) -> Any:
    if api_client is None:
        return _get_project_sessions(project_id, session_name)

    with format_api_exception(ApiException):
        response = api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id,
            name_match=session_name,
            active_only=True,
            _request_timeout=30,
        )
    sessions = response.results
    if len(sessions) == 0:
        raise ClickException(
            "No active session matching pattern {} found".format(session_name)
        )
    return sessions


# TODO (jbai): DEPRECATED - will be removed when OpenApi migration is completed
def _get_project_sessions(project_id: str, session_name: Optional[str]) -> Any:
    response = send_json_request(
        "/api/v2/sessions/",
        {"project_id": project_id, "name_match": session_name, "active_only": True},
    )
    sessions = response["results"]
    if len(sessions) == 0:
        raise ClickException(
            "No active session matching pattern {} found".format(session_name)
        )
    return sessions


def get_project_session(
    project_id: str, session_name: Optional[str], api_client: DefaultApi = None
) -> Any:
    if api_client is None:
        return _get_project_session(project_id, session_name)

    sessions = get_project_sessions(project_id, session_name, api_client)
    if len(sessions) > 1:
        raise ClickException(
            "Multiple active sessions: {}\n"
            "Please specify the one you want to refer to.".format(
                [session.name for session in sessions]
            )
        )
    return sessions[0]


# TODO (jbai): DEPRECATED - will be removed when OpenApi migration is completed
def _get_project_session(project_id: str, session_name: Optional[str]) -> Any:
    sessions = get_project_sessions(project_id, session_name)
    if len(sessions) > 1:
        raise ClickException(
            "Multiple active sessions: {}\n"
            "Please specify the one you want to refer to.".format(
                [session["name"] for session in sessions]
            )
        )
    return sessions[0]


def get_proj_name_from_id(project_id: str, api_client: DefaultApi) -> str:
    with format_api_exception(ApiException):
        resp = api_client.get_project_api_v2_projects_project_id_get(
            project_id=project_id, _request_timeout=30
        )

    if resp is None:
        raise ClickException(
            "This local project is not registered with anyscale. Please re-run `anyscale init`."
        )
    else:
        return str(resp.result.name)


def get_proj_id_from_name(
    project_name: str, api_client: Optional[DefaultApi] = None
) -> str:
    if api_client is None:
        api_client = get_api_client()

    with format_api_exception(ApiException):
        resp = api_client.find_project_by_project_name_api_v2_projects_find_by_name_get(
            name=project_name, _request_timeout=30
        )

    if not resp.results:
        raise ClickException(
            f"There is no project '{project_name}' that is registered with Anyscale. "
            "View the registered projects with `anyscale list projects`."
        )

    project = resp.results[0]
    return str(project.id)


def clone_cluster_config(
    project_name: str, directory: str, project_id: str, api_client: DefaultApi
) -> None:
    """
    Copy the cluster config from the latest session if available. Otherwise copy the
    cluster config from the project.
    """
    with format_api_exception(ApiException):
        sessions = api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id
        ).results

    if len(sessions) > 0:
        lastest_session = sessions[0]

        with format_api_exception(ApiException):
            cluster_config = api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                lastest_session.id
            ).result.config
    else:
        with format_api_exception(ApiException):
            cluster_config = api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get(
                project_id
            ).result.config

    _write_cluster_config_to_disk(project_id, cluster_config, directory)


def _write_cluster_config_to_disk(
    project_id: str, cluster_config: str, directory: str
) -> None:
    with open(os.path.join(directory, ANYSCALE_PROJECT_FILE), "w") as f:
        f.write("{}".format("project_id: {}".format(project_id)))

    cluster_config_json = json.loads(cluster_config)
    with open(os.path.join(directory, ANYSCALE_AUTOSCALER_FILE), "w") as f:
        yaml.dump(cluster_config_json, f, default_flow_style=False)


def create_new_proj_def(
    name: Optional[str],
    cluster_config_file: Optional[str],
    use_default_yaml: bool = True,
    api_client: DefaultApi = None,
) -> Tuple[str, ProjectDefinition]:
    project_name = ""
    if not name:
        while project_name == "":
            project_name = click.prompt("Project name", type=str)
            if not validate_project_name(project_name):
                print(
                    '"{}" contains spaces. Please enter a project name without spaces'.format(
                        project_name
                    ),
                    file=sys.stderr,
                )
                project_name = ""
        if not cluster_config_file:
            # TODO (yiran): Print cluster.yaml path in the else case.
            cluster_config_file = click.prompt(
                "Cluster yaml file (optional)",
                type=click.Path(exists=True),
                default=".",
                show_default=False,
            )
            if cluster_config_file == ".":
                # handling default value from prompt
                cluster_config_file = None
            else:
                use_default_yaml = False
    else:
        project_name = str(name)
    if slugify(project_name) != project_name:
        project_name = slugify(project_name)
        print("Normalized project name to {}".format(project_name))

    # Create startup.yaml.
    if cluster_config_file:
        validate_cluster_configuration(cluster_config_file, api_instance=api_client)
        if use_default_yaml and (
            not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE)
            or not os.path.samefile(
                cluster_config_file, anyscale.project.ANYSCALE_AUTOSCALER_FILE
            )
        ):
            shutil.copyfile(
                cluster_config_file, anyscale.project.ANYSCALE_AUTOSCALER_FILE
            )
    else:
        if not os.path.exists(anyscale.project.ANYSCALE_AUTOSCALER_FILE):
            with open(anyscale.project.ANYSCALE_AUTOSCALER_FILE, "w") as f:
                f.write(anyscale.project.CLUSTER_YAML_TEMPLATE)
    project_definition = anyscale.project.ProjectDefinition(os.getcwd())
    project_definition.config["name"] = project_name
    if not use_default_yaml and cluster_config_file:
        project_definition.config["cluster"]["config"] = os.path.join(
            os.getcwd(), str(cluster_config_file)
        )
    return project_name, project_definition


def register_project(
    project_definition: ProjectDefinition, api_client: DefaultApi
) -> None:
    validate_cluster_configuration(
        project_definition.cluster_yaml(), api_instance=api_client
    )

    project_name = project_definition.config["name"]
    description = project_definition.config.get("description", "")

    with open(project_definition.cluster_yaml(), "r") as f:
        initial_cluster_config = yaml.load(f, Loader=yaml.SafeLoader)

    # Add a database entry for the new Project.
    with format_api_exception(ApiException):
        resp = api_client.create_project_api_v2_projects_post(
            write_project={
                "name": project_name,
                "description": description,
                "initial_cluster_config": json.dumps(initial_cluster_config),
            }
        )
    result = resp.result
    project_id = result.id

    with open(anyscale.project.ANYSCALE_PROJECT_FILE, "w") as f:
        yaml.dump(
            {
                "project_id": project_id,
                "cluster": {"config": project_definition.cluster_yaml()},
            },
            f,
        )

    # Print success message
    url = get_endpoint(f"/projects/{project_id}")
    print(f"Project {project_id} created. View at {url}")
