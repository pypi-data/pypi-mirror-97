from datetime import datetime, timezone
import json
import os
import tempfile
from typing import Iterator, Optional, Tuple
from unittest.mock import ANY, call, Mock, mock_open, patch

import click
import pytest
import yaml

from anyscale.client.openapi_client import (  # type: ignore
    Cloud,
    CreateSessionFromSnapshotOptions,
    Project,
    ProjectDefaultSessionName,
    ProjectdefaultsessionnameResponse,
    ProjectListResponse,
    Session,
    SessionFinishUpOptions,
    SessionListResponse,
    SessionResponse,
    SessionUpOptions,
    SessionUpResponse,
    SessionupresponseResponse,
    StopSessionOptions,
)
from anyscale.controllers.session_controller import SessionController
from anyscale.project import CLUSTER_YAML_TEMPLATE


@pytest.fixture()
def mock_api_client(mock_api_client_with_session: Mock) -> Mock:
    mock_api_client = mock_api_client_with_session
    mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.return_value = (
        None
    )

    return mock_api_client


def test_stop_single_session(session_test_data: Session, mock_api_client: Mock) -> None:
    session_controller = SessionController(api_client=mock_api_client)

    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ):
        session_controller.stop(
            "test-name",
            terminate=False,
            delete=False,
            workers_only=False,
            keep_min_workers=False,
        )

    mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.assert_called_once_with(
        session_test_data.id,
        StopSessionOptions(
            terminate=False, delete=False, workers_only=False, keep_min_workers=False
        ),
    )

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")


@pytest.fixture()
def mock_api_client_multiple_sessions(base_mock_api_client: Mock) -> Mock:
    base_mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[
            Session(
                id="ses_1",
                name="session_name",
                created_at=datetime.now(tz=timezone.utc),
                snapshots_history=[],
                tensorboard_available=False,
                project_id="project_id",
                state="Running",
                head_node_ip="127.0.0.1",
                idle_timeout=120,
            ),
            Session(
                id="ses_2",
                name="session_name2",
                created_at=datetime.now(tz=timezone.utc),
                snapshots_history=[],
                tensorboard_available=False,
                project_id="project_id",
                state="Running",
                head_node_ip="127.0.0.1",
                idle_timeout=120,
            ),
        ]
    )
    base_mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.return_value = (
        None
    )
    base_mock_api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.return_value.result.head_ip = (
        "127.0.0.1"
    )

    return base_mock_api_client


def test_stop_multiple_sessions(mock_api_client_multiple_sessions: Mock) -> None:
    mock_api_client = mock_api_client_multiple_sessions
    session_controller = SessionController(api_client=mock_api_client)

    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value="project_id")

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ):
        session_controller.stop(
            "ses_?",
            terminate=True,
            delete=True,
            workers_only=True,
            keep_min_workers=True,
        )

    mock_api_client.stop_session_api_v2_sessions_session_id_stop_post.assert_has_calls(
        [
            call(
                "ses_1",
                StopSessionOptions(
                    terminate=True,
                    delete=True,
                    workers_only=True,
                    keep_min_workers=True,
                ),
            ),
            call(
                "ses_2",
                StopSessionOptions(
                    terminate=True,
                    delete=True,
                    workers_only=True,
                    keep_min_workers=True,
                ),
            ),
        ]
    )

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")


@pytest.fixture()
def mock_up_tuple(
    base_mock_api_client: Mock,
    project_test_data: Project,
    cloud_test_data: Cloud,
    session_test_data: Session,
) -> Iterator[Tuple[Mock, Project, Cloud, Mock]]:
    base_mock_api_client.get_session_api_v2_sessions_session_id_get = Mock(
        return_value=SessionResponse(result=session_test_data)
    )
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_popen_output = Mock()
    mock_popen_output.stdout = []
    mock_popen_output.returncode = 0
    mock_popen_output.communicate = Mock()
    subprocess_mock = Mock(return_value=mock_popen_output)
    mock_wait_for_session_start = Mock()

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=Mock(return_value=mock_project_definition),
        get_project_id=Mock(return_value=project_test_data.id),
        get_cloud_id_and_name=Mock(
            return_value=tuple([cloud_test_data.id, cloud_test_data.name])
        ),
        download_anyscale_wheel=Mock(return_value=None),
        configure_for_session=Mock(return_value=yaml.safe_load(CLUSTER_YAML_TEMPLATE),),
        get_head_node_ip=Mock(return_value="1.2.3.4"),
        wait_for_session_start=mock_wait_for_session_start,
    ), patch.multiple("subprocess", Popen=subprocess_mock):
        yield base_mock_api_client, project_test_data, cloud_test_data, mock_wait_for_session_start


def test_anyscale_up_success(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple
    session_controller = SessionController(api_client=mock_api_client)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[]  # No session with this name yet, brand new session.
    )
    # Session Name should be "11"
    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id="session-10",
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )
    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        temp_file.write(CLUSTER_YAML_TEMPLATE)
        temp_file.flush()

        session_controller.up(
            session_name=None,
            config=temp_file.name,
            build_id=None,
            compute_template_id=None,
            min_workers=None,
            max_workers=None,
            no_restart=False,
            restart_only=False,
            disable_sync=False,
            cloud_id=None,
            cloud_name=None,
            idle_timeout=-1,
            yes=True,
        )
        mock_api_client.session_up_api_v2_sessions_up_post.assert_called_with(
            session_up_options=SessionUpOptions(
                project_id=project_test_data.id,
                name="session-11",
                cluster_config={
                    "config": json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))
                },
                cloud_id=cloud_test_data.id,
                idle_timeout=-1,
            )
        )

    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_once()


def test_anyscale_up_templates_success(
    mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]
) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple

    session_controller = SessionController(api_client=mock_api_client)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[]  # No session with this name yet, brand new session.
    )

    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id="session-10",
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )

    session_controller.up(
        session_name=None,
        config=None,
        build_id="build-id",
        compute_template_id="ct-id",
        min_workers=None,
        max_workers=None,
        idle_timeout=-1,
        no_restart=False,
        restart_only=False,
        disable_sync=False,
        cloud_id=None,
        cloud_name=None,
        yes=True,
    )
    # Ensure that the API call is made with the
    # build ID and compute template ID,
    # and not the cluster config.
    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_with(
        session_up_options=SessionUpOptions(
            project_id=project_test_data.id,
            name="session-11",
            cluster_config=None,
            idle_timeout=-1,
            build_id="build-id",
            compute_template_id="ct-id",
            cloud_id=cloud_test_data.id,
        )
    )
    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_once()


def test_anyscale_up_templates_badparams(
    mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]
) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple

    session_controller = SessionController(api_client=mock_api_client)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[]  # No session with this name yet, brand new session.
    )

    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id="session-10",
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )

    # Specifying only the build ID or only the compute template ID
    # should raise a ValueError.
    # (If neither are specified, it counts as a cluster config
    # startup path, and is handled in other existing tests.)
    with pytest.raises(ValueError):
        session_controller.up(
            session_name=None,
            config=None,
            build_id="build-id",
            compute_template_id=None,
            min_workers=None,
            max_workers=None,
            idle_timeout=-1,
            no_restart=False,
            restart_only=False,
            disable_sync=False,
            cloud_id=None,
            cloud_name=None,
            yes=True,
        )

    with pytest.raises(ValueError):
        session_controller.up(
            session_name=None,
            config=None,
            build_id=None,
            compute_template_id="ct-id",
            min_workers=None,
            max_workers=None,
            idle_timeout=-1,
            no_restart=False,
            restart_only=False,
            disable_sync=False,
            cloud_id=None,
            cloud_name=None,
            yes=True,
        )


def test_anyscale_up_failure(mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple
    session_controller = SessionController(api_client=mock_api_client)
    sesion_id = "session-10"
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[]  # No session with this name yet, brand new session.
    )
    # Session Name should be "11"
    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id=sesion_id,
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )
    mock_wait_for_start.side_effect = click.ClickException("Node Failed to Start!")

    # We are setting the mock to return an error code
    import subprocess

    subprocess.Popen.return_value.returncode = 100  # type: ignore

    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        temp_file.write(CLUSTER_YAML_TEMPLATE)
        temp_file.flush()
        with pytest.raises(click.ClickException):
            session_controller.up(
                session_name=None,
                config=temp_file.name,
                build_id=None,
                compute_template_id=None,
                min_workers=None,
                max_workers=None,
                no_restart=False,
                restart_only=False,
                disable_sync=False,
                cloud_id=None,
                cloud_name=None,
                idle_timeout=-1,
                yes=True,
            )
        mock_api_client.session_finish_up_api_v2_sessions_session_id_finish_up_post.assert_called_once_with(
            session_finish_up_options=SessionFinishUpOptions(
                startup_log="",
                new_session=True,
                head_node_ip="1.2.3.4",
                cluster_launch_errored=True,
            ),
            session_id=sesion_id,
        )


def test_anyscale_up_no_config_provided(
    mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]
) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple
    session_controller = SessionController(api_client=mock_api_client)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[
            Session
        ]  # This session already exists so no config needs to be provided
    )
    # Session Name should be "11"
    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id="session-10",
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )
    session_controller.up(
        session_name=None,
        config=None,
        build_id=None,
        compute_template_id=None,
        min_workers=None,
        max_workers=None,
        no_restart=False,
        restart_only=False,
        disable_sync=False,
        cloud_id=None,
        cloud_name=None,
        idle_timeout=-1,
        yes=True,
    )
    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_with(
        session_up_options=SessionUpOptions(
            project_id=project_test_data.id,
            name="session-11",
            cluster_config=None,
            cloud_id=cloud_test_data.id,
            idle_timeout=-1,
        )
    )

    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_once()


def test_anyscale_up_config_provided(
    mock_up_tuple: Tuple[Mock, Project, Cloud, Mock]
) -> None:
    (
        mock_api_client,
        project_test_data,
        cloud_test_data,
        mock_wait_for_start,
    ) = mock_up_tuple
    session_controller = SessionController(api_client=mock_api_client)
    mock_api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get.return_value = ProjectdefaultsessionnameResponse(
        result=ProjectDefaultSessionName(name="session-11")
    )
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[
            Session
        ]  # This session already exists so no config needs to be provided
    )
    # Session Name should be "11"
    mock_api_client.session_up_api_v2_sessions_up_post = Mock(
        return_value=SessionupresponseResponse(
            result=SessionUpResponse(
                session_id="session-10",
                cluster_name="new_cluster",
                private_key="key",
                cluster_config=yaml.safe_load(CLUSTER_YAML_TEMPLATE),
                is_same_cluster_config=False,
            )
        )
    )
    with tempfile.NamedTemporaryFile(mode="w") as temp_file:
        temp_file.write(CLUSTER_YAML_TEMPLATE)
        temp_file.flush()

        session_controller.up(
            session_name=None,
            config=temp_file.name,
            build_id=None,
            compute_template_id=None,
            min_workers=None,
            max_workers=None,
            no_restart=False,
            restart_only=False,
            disable_sync=False,
            cloud_id=None,
            cloud_name=None,
            idle_timeout=-1,
            yes=True,
        )
        mock_api_client.session_up_api_v2_sessions_up_post.assert_called_with(
            session_up_options=SessionUpOptions(
                project_id=project_test_data.id,
                name="session-11",
                cluster_config={
                    "config": json.dumps(yaml.safe_load(CLUSTER_YAML_TEMPLATE))
                },
                cloud_id=cloud_test_data.id,
                idle_timeout=-1,
            )
        )

    mock_api_client.session_up_api_v2_sessions_up_post.assert_called_once()


def test_ssh_session(
    session_test_data: Session, mock_api_client_multiple_sessions: Mock
) -> None:
    session_controller = SessionController(api_client=mock_api_client_multiple_sessions)

    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    mock_get_cluster_config = Mock(
        return_value={"auth": {"ssh_user": "", "ssh_private_key": ""}}
    )

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
        get_cluster_config=mock_get_cluster_config,
        get_project_session=mock_get_project_session,
    ), patch.multiple("subprocess", run=Mock()):
        session_controller.ssh(session_name=session_test_data.name, ssh_option=("",))

    mock_api_client_multiple_sessions.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.assert_called_once_with(
        session_test_data.id,
    )

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")
    mock_get_cluster_config.assert_called_once_with(
        session_test_data.name, mock_api_client_multiple_sessions
    )


def test_autopush(
    session_test_data: Session, mock_api_client_with_session: Mock
) -> None:
    mock_api_client_with_session.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.return_value.result.head_ip = (
        "127.0.0.1"
    )

    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    cluster_config_data = {"auth": {"ssh_user": "", "ssh_private_key": ""}}
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_wait_for_session_start = Mock()
    mock_get_working_dir = Mock(return_value="")
    mock_managed_autosync_session = Mock()
    mock_managed_autosync_session.return_value.__enter__ = Mock(
        return_value=(Mock(), None)
    )
    mock_managed_autosync_session.return_value.__exit__ = Mock(return_value=None)
    mock_perform_autopush_synchronization = Mock()
    mock_perform_sync = Mock()
    mock_perform_sync.return_value.returncode = 0

    session_controller = SessionController(api_client=mock_api_client_with_session)

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
        get_cluster_config=mock_get_cluster_config,
        get_project_session=mock_get_project_session,
        get_working_dir=mock_get_working_dir,
        managed_autosync_session=mock_managed_autosync_session,
        perform_sync=mock_perform_sync,
        wait_for_session_start=mock_wait_for_session_start,
        perform_autopush_synchronization=mock_perform_autopush_synchronization,
    ):
        session_controller.autopush(session_name=session_test_data.name)

    mock_api_client_with_session.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.assert_called_once_with(
        session_test_data.id,
    )

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")
    mock_get_project_session.assert_called_once_with(
        session_test_data.project_id,
        session_test_data.name,
        mock_api_client_with_session,
    )
    mock_get_cluster_config.assert_called_once_with(
        session_test_data.name, mock_api_client_with_session
    )
    mock_wait_for_session_start.assert_called_once_with(
        session_test_data.project_id,
        session_test_data.name,
        mock_api_client_with_session,
    )
    mock_get_working_dir.assert_called_once_with(
        cluster_config_data, session_test_data.project_id, mock_api_client_with_session
    )
    mock_managed_autosync_session.assert_called_once_with(
        session_test_data.id, mock_api_client_with_session
    )
    mock_perform_sync.assert_called_once_with(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile={}".format(os.devnull),
            "-o",
            "LogLevel=ERROR",
            "-i",
            "",
        ],
        mock_project_definition.root,
        "",
        "127.0.0.1",
        "",
        False,
        rsync_exclude=[],
        rsync_filter=[],
    )
    mock_perform_autopush_synchronization.assert_called_once()


def test_autosync_docker(
    session_test_data: Session, mock_api_client_with_session: Mock
) -> None:
    mock_api_client_with_session.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.return_value.result.head_ip = (
        "127.0.0.1"
    )

    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    cluster_config_data = {"auth": {"ssh_user": "", "ssh_private_key": ""}}
    cluster_config_data["docker"] = {
        "image": "rayproject/ray:latest",
        "container_name": "ray_container",
    }
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_wait_for_session_start = Mock()
    mock_get_working_dir = Mock(return_value="/working_dir")
    mock_managed_autosync_session = Mock()
    mock_managed_autosync_session.return_value.__enter__ = Mock(
        return_value=(Mock(), None)
    )
    mock_managed_autosync_session.return_value.__exit__ = Mock(return_value=None)
    mock_perform_autopush_synchronization = Mock()
    mock_perform_sync = Mock()
    mock_perform_sync.return_value.returncode = 0

    session_controller = SessionController(api_client=mock_api_client_with_session)

    remote_location = "/fake/host/mount"
    mock_subprocess_run = Mock()
    mock_subprocess_run.return_value.stdout = json.dumps(
        [{"Source": remote_location, "Destination": "/working_dir"}]
    )

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
        get_cluster_config=mock_get_cluster_config,
        get_project_session=mock_get_project_session,
        get_working_dir=mock_get_working_dir,
        managed_autosync_session=mock_managed_autosync_session,
        perform_sync=mock_perform_sync,
        wait_for_session_start=mock_wait_for_session_start,
        perform_autopush_synchronization=mock_perform_autopush_synchronization,
    ), patch.multiple("subprocess", run=mock_subprocess_run):
        session_controller.autopush(session_name=session_test_data.name)

    mock_api_client_with_session.get_session_head_ip_api_v2_sessions_session_id_head_ip_get.assert_called_once_with(
        session_test_data.id,
    )

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")
    mock_get_project_session.assert_called_once_with(
        session_test_data.project_id,
        session_test_data.name,
        mock_api_client_with_session,
    )
    mock_get_cluster_config.assert_called_once_with(
        session_test_data.name, mock_api_client_with_session
    )
    mock_wait_for_session_start.assert_called_once_with(
        session_test_data.project_id,
        session_test_data.name,
        mock_api_client_with_session,
    )
    mock_get_working_dir.assert_called_once_with(
        cluster_config_data, session_test_data.project_id, mock_api_client_with_session
    )
    mock_managed_autosync_session.assert_called_once_with(
        session_test_data.id, mock_api_client_with_session
    )
    mock_perform_sync.assert_called_once_with(
        [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile={}".format(os.devnull),
            "-o",
            "LogLevel=ERROR",
            "-i",
            "",
        ],
        mock_project_definition.root,
        "",
        "127.0.0.1",
        remote_location,
        False,
        rsync_exclude=[],
        rsync_filter=[],
    )
    mock_perform_autopush_synchronization.assert_called_once()


def test_anyscale_push_session(
    session_test_data: Session, mock_api_client_with_session: Mock
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    mock_get_project_session = Mock(return_value=session_test_data)
    cluster_config_data = {"auth": {"ssh_user": "", "ssh_private_key": ""}}
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_managed_autosync_session = Mock()
    mock_managed_autosync_session.return_value.__enter__ = Mock(
        return_value=(Mock(), None)
    )
    mock_managed_autosync_session.return_value.__exit__ = Mock(return_value=None)
    mock_subprocess_run = Mock()
    mock_subprocess_run.return_value.returncode = 0

    mock_validate_cluster_configuration = Mock()
    mock_rsync = Mock()
    mock_up = Mock()

    session_controller = SessionController(api_client=mock_api_client_with_session)

    with patch.multiple("subprocess", run=mock_subprocess_run), patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
        get_cluster_config=mock_get_cluster_config,
        get_project_session=mock_get_project_session,
        validate_cluster_configuration=mock_validate_cluster_configuration,
        rsync=mock_rsync,
    ), patch.object(session_controller, "up", new=mock_up):
        session_name = "TestSessionName"
        source = "TestSource"
        target = "TestTarget"
        config = "TestConfig"
        all_nodes = True
        session_controller.push(session_name, source, target, config, all_nodes)

        # Don't check the config_file argument because it's a random path of
        # a temporary file
        mock_rsync.assert_called_once_with(
            ANY, source=source, target=target, down=False,
        )

        mock_validate_cluster_configuration.assert_called_once_with(
            config, api_instance=mock_api_client_with_session
        )

        mock_up.assert_called_once_with(
            session_name=session_test_data.name,
            config=None,
            build_id=None,
            compute_template_id=None,
            min_workers=None,
            max_workers=None,
            no_restart=False,
            idle_timeout=None,
            restart_only=False,
            disable_sync=True,
            cloud_id=session_test_data.cloud_id,
            cloud_name=None,
            yes=True,
        )


@pytest.mark.parametrize("config", [None, "tmp.yaml"])
def test_pull(
    session_test_data: Session, mock_api_client_with_session: Mock, config: str
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)
    mock_get_project_id = Mock(return_value=session_test_data.project_id)
    cluster_config_data = {"auth": {"ssh_user": "", "ssh_private_key": ""}}
    mock_get_cluster_config = Mock(return_value=cluster_config_data)
    mock_get_working_dir = Mock(return_value="directory")
    mock_rsync = Mock()
    mock_get_project_session = Mock(return_value=session_test_data)
    mock_api_client_with_session.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.return_value.result.config_with_defaults = (
        "temp"
    )

    session_controller = SessionController(api_client=mock_api_client_with_session)

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
        get_cluster_config=mock_get_cluster_config,
        get_working_dir=mock_get_working_dir,
        get_project_session=mock_get_project_session,
        rsync=mock_rsync,
    ), patch("builtins.open", new_callable=mock_open()), patch("yaml.dump"):
        session_controller.pull(session_name=session_test_data.name, config=config)

    mock_load_project_or_throw.assert_called_once_with()
    mock_get_project_id.assert_called_once_with("/some/directory")
    mock_get_cluster_config.assert_called_once_with(
        session_test_data.name, mock_api_client_with_session
    )
    mock_get_working_dir.assert_called_once_with(
        cluster_config_data, session_test_data.project_id, mock_api_client_with_session
    )
    mock_rsync.assert_called_once()
    if config:
        mock_get_project_session.assert_called_once_with(
            session_test_data.project_id,
            session_test_data.name,
            mock_api_client_with_session,
        )
        mock_api_client_with_session.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.assert_called_once_with(
            session_test_data.id
        )


@pytest.mark.parametrize("project_name", ["project_name", None])
def test_fork_session(
    session_test_data: Session,
    mock_api_client_with_session: Mock,
    project_name: Optional[str],
) -> None:

    with patch.object(
        SessionController, "_resolve_session", return_value=session_test_data
    ) as mock_resolve_session, patch.object(
        SessionController, "_fork_session_internal", return_value=session_test_data
    ) as mock_fork_session_internal:
        session_controller = SessionController(mock_api_client_with_session)
        output_str = session_controller.fork_session(
            "session_name", "new_session_name", project_name
        )

    mock_resolve_session.assert_called_once_with("session_name", project_name)
    mock_fork_session_internal.assert_called_once_with(
        session_test_data, "new_session_name"
    )

    url = f"https://beta.anyscale.com/projects/{session_test_data.project_id}/sessions/{session_test_data.id}"
    assert output_str == f"Session {session_test_data.name} started. View at {url}"


@pytest.mark.parametrize("project_name", [None, "project_name"])
def test_resolve_session(
    project_test_data: Project,
    session_test_data: Session,
    mock_api_client_with_session: Mock,
    project_name: Optional[str],
) -> None:
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value=session_test_data.project_id)

    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_test_data]
    )
    mock_api_client_with_session.list_projects_api_v2_projects_get.return_value = ProjectListResponse(
        results=[project_test_data]
    )

    with patch.multiple(
        "anyscale.controllers.session_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ):
        session_controller = SessionController(mock_api_client_with_session)
        session = session_controller._resolve_session("session_name", project_name)

    assert session == session_test_data

    if project_name:
        mock_load_project_or_throw.assert_not_called()
        mock_get_project_id.assert_not_called()
        mock_api_client_with_session.list_projects_api_v2_projects_get.assert_called_once_with()
    else:
        mock_load_project_or_throw.assert_called_once()
        mock_get_project_id.assert_called_once_with(mock_project_definition.root)
        mock_api_client_with_session.list_projects_api_v2_projects_get.assert_not_called()

    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_once_with(
        session_test_data.project_id, name="session_name"
    )


def test_fork_session_internal(
    session_test_data: Session, mock_api_client_with_session: Mock
) -> None:
    mock_api_client_with_session.fork_session_api_v2_sessions_session_id_fork_post.return_value = (
        None
    )
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_test_data]
    )

    session_controller = SessionController(mock_api_client_with_session)
    cloned_session = session_controller._fork_session_internal(
        session_test_data, "new_session_name"
    )

    assert cloned_session == session_test_data

    mock_api_client_with_session.fork_session_api_v2_sessions_session_id_fork_post.assert_called_once_with(
        session_id=session_test_data.id,
        create_session_from_snapshot_options=CreateSessionFromSnapshotOptions(
            project_id=session_test_data.project_id, name="new_session_name"
        ),
        _request_timeout=300000,
    )
    mock_api_client_with_session.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id, name="new_session_name"
    )
