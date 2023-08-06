from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client.models.execute_command_response import ExecuteCommandResponse  # type: ignore
from anyscale.client.openapi_client.models.execute_interactive_command_options import (  # type: ignore
    ExecuteInteractiveCommandOptions,
)
from anyscale.client.openapi_client.models.executecommandresponse_response import ExecutecommandresponseResponse  # type: ignore
from anyscale.controllers.exec_controller import ExecController


@pytest.fixture()
def mock_api_client(command_id_test_data: ExecuteCommandResponse) -> Mock:
    mock_api_client = Mock()

    mock_api_client.execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post = Mock(
        return_value=ExecutecommandresponseResponse(result=command_id_test_data)
    )

    return mock_api_client


def test_anyscale_exec(
    mock_api_client: Mock, command_id_test_data: ExecuteCommandResponse
) -> None:
    mock_cluster_config = {"provider": {"default": "value"}, "cluster_name": "cname"}
    mock_get_cluster_config = Mock(return_value=mock_cluster_config)
    mock_rsync = Mock(return_value=None)
    mock_check_call = Mock(return_value=None)
    mock_click_echo = Mock(return_value=None)

    with patch.object(
        ExecController,
        "_get_session_name_and_id",
        return_value=("session_name", "session_id"),
    ) as mock_get_session_name_and_id, patch.object(
        ExecController, "_generate_remote_command", return_value="remote_command"
    ) as mock_generate_remote_command, patch.multiple(
        "anyscale.controllers.exec_controller",
        get_cluster_config=mock_get_cluster_config,
        rsync=mock_rsync,
    ), patch.multiple(
        "subprocess", check_call=mock_check_call
    ), patch.multiple(
        "click", echo=mock_click_echo
    ):
        commands = ["cmd1", "cmd2"]
        exec_controller = ExecController(api_client=mock_api_client)
        exec_controller.anyscale_exec(
            "session_name", True, False, (1000,), True, True, False, commands
        )

    mock_api_client.execute_interactive_command_api_v2_sessions_session_id_execute_interactive_command_post.assert_called_once_with(
        session_id="session_id",
        execute_interactive_command_options=ExecuteInteractiveCommandOptions(
            shell_command=" ".join(commands)
        ),
    )
    mock_get_session_name_and_id.assert_called_once_with("session_name")
    mock_generate_remote_command.assert_called_once_with(
        command_id_test_data.command_id,
        commands,
        command_id_test_data.directory_name,
        True,
        False,
    )
    mock_get_cluster_config.assert_called_once_with("session_name", mock_api_client)
    mock_rsync.assert_called_once()
    mock_check_call.assert_called_once()
    mock_click_echo.assert_called_once()
