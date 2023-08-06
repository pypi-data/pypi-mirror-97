from datetime import datetime, timezone
from typing import Any
from unittest.mock import Mock, patch


import pytest

from anyscale.client.openapi_client import (  # type: ignore
    Cloud,
    ExecuteCommandResponse,
    Project,
    Session,
    SessionCommand,
    SessionCommandTypes,
    SessionListResponse,
    SessionStartingUpData,
    SessionStateData,
)


@pytest.fixture()
def base_mock_api_client() -> Mock:
    mock_api_client = Mock()
    return mock_api_client


@pytest.fixture()
def mock_api_client_with_session(
    base_mock_api_client: Mock, session_test_data: Session
) -> Mock:
    base_mock_api_client.list_sessions_api_v2_sessions_get.return_value = SessionListResponse(
        results=[session_test_data]
    )
    return base_mock_api_client


@pytest.fixture(scope="module")
def cloud_test_data() -> Cloud:
    return Cloud(
        id="cloud_id_1",
        name="cloud_name_1",
        provider="provider",
        region="region",
        credentials="credentials",
        creator_id="creator_id",
        type="PUBLIC",
        created_at=datetime.now(timezone.utc),
        config='{"max_stopped_instances": 0}',
    )


@pytest.fixture(scope="module")
def project_test_data() -> Project:
    return Project(
        name="project_name",
        description="test project",
        cloud_id="cloud_id",
        initial_cluster_config="initial_config",
        id="project_id",
        created_at=datetime.now(tz=timezone.utc),
        creator_id="creator_id",
        is_owner=True,
        directory_name="/directory/name",
        active_sessions=0,
        last_activity_at=datetime.now(tz=timezone.utc),
    )


@pytest.fixture(scope="module")
def session_test_data() -> Session:
    return Session(
        id="session_id",
        name="session_name",
        created_at=datetime.now(tz=timezone.utc),
        snapshots_history=[],
        tensorboard_available=False,
        project_id="project_id",
        state="Running",
        idle_timeout=120,
    )


@pytest.fixture(scope="module")
def session_start_error_test_data() -> Session:
    return Session(
        id="session_id",
        name="session_name",
        created_at=datetime.now(tz=timezone.utc),
        snapshots_history=[],
        tensorboard_available=False,
        project_id="project_id",
        state="StartupErrored",
        state_data=SessionStateData(
            startup=SessionStartingUpData(startup_error="start up error")
        ),
        idle_timeout=120,
    )


@pytest.fixture(scope="module")
def session_terminated_test_data() -> Session:
    return Session(
        id="session_id",
        name="session_name",
        created_at=datetime.now(tz=timezone.utc),
        snapshots_history=[],
        tensorboard_available=False,
        project_id="project_id",
        state="Terminated",
        idle_timeout=120,
    )


@pytest.fixture(scope="module")
def session_command_test_data() -> SessionCommand:
    return SessionCommand(
        id="session_command_id",
        created_at=datetime.now(tz=timezone.utc),
        name="session_command",
        params="params",
        shell="shell",
        shell_command="shell_command",
        type=SessionCommandTypes.COMMAND_LINE_RUNNER,
    )


@pytest.fixture(scope="module")
def command_id_test_data() -> ExecuteCommandResponse:
    return ExecuteCommandResponse(
        command_id="command_id",
        directory_name="dir_name",
        dns_address="session.anyscaleuserdata-dev.com",
    )


@pytest.fixture(scope="session", autouse=True)
def default_session_fixture(
    request: "_pytest.fixtures.SubRequest",  # type: ignore # noqa: F821
) -> Any:
    with patch("time.sleep", Mock()):
        yield
