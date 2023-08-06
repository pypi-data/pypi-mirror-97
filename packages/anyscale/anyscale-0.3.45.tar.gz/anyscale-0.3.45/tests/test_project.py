import json
import os
from unittest.mock import ANY, Mock, mock_open, patch

from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.client.openapi_client.models.project_response import ProjectResponse  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.client.openapi_client.models.session_list_response import SessionListResponse  # type: ignore
from anyscale.project import (
    clone_cluster_config,
    create_new_proj_def,
    get_proj_id_from_name,
    get_proj_name_from_id,
    get_project_session,
    get_project_sessions,
    ProjectDefinition,
    register_project,
)


def test_get_project_sessions(session_test_data: Session) -> None:
    mock_api_client = Mock()
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_test_data]
    )

    sessions = get_project_sessions(session_test_data.project_id, None, mock_api_client)

    assert sessions == [session_test_data]
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id,
        name_match=None,
        active_only=True,
        _request_timeout=ANY,
    )


def test_get_project_session(session_test_data: Session) -> None:
    mock_api_client = Mock()
    mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_test_data]
    )

    session = get_project_session(session_test_data.project_id, None, mock_api_client)

    assert session == session_test_data
    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=session_test_data.project_id,
        name_match=None,
        active_only=True,
        _request_timeout=ANY,
    )


def test_get_proj_name_from_id(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.get_project_api_v2_projects_project_id_get.return_value = ProjectResponse(
        result=project_test_data
    )
    project_name = get_proj_name_from_id(project_test_data.id, mock_api_client)

    assert project_name == project_test_data.name
    mock_api_client.get_project_api_v2_projects_project_id_get.assert_called_once_with(
        project_id=project_test_data.id, _request_timeout=ANY,
    )


def test_get_proj_id_from_name(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.return_value.results = [
        project_test_data
    ]
    project_id = get_proj_id_from_name(project_test_data.name, mock_api_client)

    assert project_id == project_test_data.id
    mock_api_client.find_project_by_project_name_api_v2_projects_find_by_name_get.assert_called_once_with(
        name=project_test_data.name, _request_timeout=ANY,
    )


def test_clone_config_from_project(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.list_sessions_api_v2_sessions_get.return_value.results = []
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.return_value.result.config = (
        ""
    )
    with patch(
        "anyscale.project._write_cluster_config_to_disk"
    ) as write_cluster_config_mock:
        clone_cluster_config(
            project_test_data.name,
            project_test_data.directory_name,
            project_test_data.id,
            mock_api_client,
        )

    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=project_test_data.id
    )
    mock_api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get.assert_called_once_with(
        project_test_data.id
    )
    write_cluster_config_mock.assert_called_once_with(
        project_test_data.id, "", project_test_data.directory_name
    )


def test_clone_config_from_session(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_session = Mock(id=1)
    mock_api_client.list_sessions_api_v2_sessions_get.return_value.results = [
        mock_session
    ]
    mock_api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.return_value.result.config = (
        ""
    )
    with patch(
        "anyscale.project._write_cluster_config_to_disk"
    ) as write_cluster_config_mock:
        clone_cluster_config(
            project_test_data.name,
            project_test_data.directory_name,
            project_test_data.id,
            mock_api_client,
        )

    mock_api_client.list_sessions_api_v2_sessions_get.assert_called_once_with(
        project_id=project_test_data.id
    )
    mock_api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get.assert_called_once_with(
        mock_session.id
    )
    write_cluster_config_mock.assert_called_once_with(
        project_test_data.id, "", project_test_data.directory_name
    )


def test_create_new_proj_def(project_test_data: Project) -> None:
    mock_api_client = Mock()

    with patch("builtins.open", new_callable=mock_open()), patch(
        "anyscale.project.validate_cluster_configuration"
    ) as validate_cluster_configuration_mock, patch("shutil.copyfile"), patch(
        "os.path.samefile"
    ):
        project_name, project_definition = create_new_proj_def(
            project_test_data.name,
            "tmp.yaml",
            use_default_yaml=False,
            api_client=mock_api_client,
        )

    assert project_name == project_test_data.name
    assert os.path.normpath(project_definition.root) == os.getcwd()
    assert os.path.normpath(
        project_definition.config["cluster"]["config"]
    ) == os.path.join(os.getcwd(), "tmp.yaml")
    validate_cluster_configuration_mock.assert_called_once_with(
        "tmp.yaml", api_instance=mock_api_client
    )


def test_register_project(project_test_data: Project) -> None:
    mock_api_client = Mock()
    mock_api_client.create_project_api_v2_projects_post.return_value.result.id = (
        project_test_data.id
    )
    mock_yaml_load = Mock()
    mock_yaml_load.return_value = project_test_data.initial_cluster_config

    project_definition = ProjectDefinition(os.getcwd())
    project_definition.config["name"] = project_test_data.name

    with patch("builtins.open", new_callable=mock_open()), patch(
        "anyscale.project.validate_cluster_configuration"
    ) as validate_cluster_configuration_mock, patch("yaml.load", mock_yaml_load):
        register_project(project_definition, mock_api_client)

    validate_cluster_configuration_mock.assert_called_once_with(
        project_definition.cluster_yaml(), api_instance=mock_api_client
    )
    mock_api_client.create_project_api_v2_projects_post.assert_called_once_with(
        write_project={
            "name": project_test_data.name,
            "description": "",
            "initial_cluster_config": json.dumps(
                project_test_data.initial_cluster_config
            ),
        }
    )
