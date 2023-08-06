import json
import logging
import os
import shutil
from typing import Any, List, Optional

import click
import requests

from anyscale.client.openapi_client.rest import ApiException  # type: ignore
from anyscale.project import get_project_id, ProjectDefinition
from anyscale.util import (
    format_api_exception,
    get_cluster_config,
    send_json_request,
)


logger = logging.getLogger(__file__)


def copy_file(to_s3: bool, source: str, target: Any, download: bool) -> None:
    """Copy a file.

    The file source or target may be on S3.

    Args:
        to_s3 (bool): If this is True, then copy to/from S3, else the local
            disk. If this is True, then the file source or target will be a
            presigned URL to which GET or POST HTTP requests can be sent.
        source (str or S3 URL): Source file local pathname or S3 GET URL. If
            this is an S3 URL, target is assumed to be a local pathname.
        target (str or S3 URL): Target file local pathname or S3 URL with POST
            credentials. If this is an S3 URL, source is assumed to be a local
            pathname.
        download (bool): If this is True, then this will upload from source to
            target, else this will download.
    """
    try:
        if to_s3:
            if download:
                with open(target, "wb") as f:
                    response = requests.get(source)
                    for block in response.iter_content(1024):
                        f.write(block)
            else:
                with open(source, "rb") as f:
                    files = {"file": ("object", f)}
                    resp = requests.post(
                        target["url"], data=target["fields"], files=files
                    )
                    assert resp.ok, resp.text
        else:
            shutil.copyfile(source, target)
    except (OSError, AssertionError) as e:
        logger.warn("Failed to copy file %s , aborting", source)
        raise e


def create_snapshot(
    project_definition: ProjectDefinition,
    yes: bool,
    description: Optional[str] = None,
    tags: List[str] = [],
    api_instance: Optional[Any] = None,
) -> str:
    """Create a snapshot of a project.

    Args:
        project_definition: Project definition.
        yes: Don't ask for confirmation.
        description: An optional description of the snapshot.
        tags: Tags for the snapshot.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
        Exception: If saving the snapshot files fails.
    """
    # Find and validate the current project ID.
    project_dir = project_definition.root
    project_id = get_project_id(project_dir)

    cluster_config = get_cluster_config(
        os.path.join(project_dir, project_definition.cluster_yaml())
    )

    if api_instance:
        with format_api_exception(ApiException):
            resp = api_instance.create_snapshot_api_v2_snapshots_post(
                create_snapshot_options={
                    "project_id": project_id,
                    "cluster_config": json.dumps(cluster_config),
                    "description": description if description else "",
                    "tags": tags,
                }
            )
        snapshot_id = resp.result.id
    else:
        resp = send_json_request(
            "/api/v2/snapshots/",
            {
                "project_id": project_id,
                "cluster_config": json.dumps(cluster_config),
                "description": description if description else "",
                "tags": tags,
            },
            method="POST",
        )
        snapshot_id = resp["result"]["id"]
    return str(snapshot_id)


def describe_snapshot(snapshot_id: str) -> Any:
    resp = send_json_request("/api/v2/snapshots/{}".format(snapshot_id), {})
    return resp["result"]


def list_snapshots(project_dir: str) -> List[str]:
    """List all snapshots associated with the given project.

    Args:
        project_dir: Project root directory.

    Returns:
        List of Snapshots for the current project.

    Raises:
        ValueError: If the current project directory does not match the project
            metadata entry in the database.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    return [snapshot["id"] for snapshot in snapshots]


def get_snapshot_id(project_dir: str, snapshot_id: str) -> str:
    """Get a snapshot of the given project with the given name.

    Args:
        project_id: The ID of the project.
        snapshot_name: The name of the snapshot to get. If there are multiple
            snapshots with the same name, then the user will be prompted to
            choose a snapshot.
    """
    # Find and validate the current project ID.
    project_id = get_project_id(project_dir)
    resp = send_json_request("/api/v2/snapshots/", {"project_id": project_id})
    snapshots = resp["result"]["snapshots"]
    if len(snapshots) == 0:
        raise ValueError("No snapshots found with name {}".format(snapshot_id))
    snapshot_idx = 0
    if len(snapshots) > 1:
        print(
            "More than one snapshot found with ID {}. "
            "Which do you want to use?".format(snapshot_id)
        )
        for i, snapshot in enumerate(snapshots):
            print("{}. {}".format(i + 1, snapshot["id"]))
        snapshot_idx = click.prompt(
            "Please enter a snapshot number from 1 to {}".format(len(snapshots)),
            type=int,
        )
        snapshot_idx -= 1
        if snapshot_idx < 0 or snapshot_idx > len(snapshots):
            raise ValueError("Snapshot index {} is out of range".format(snapshot_idx))
    result: str = snapshots[snapshot_idx]["id"]
    return result
