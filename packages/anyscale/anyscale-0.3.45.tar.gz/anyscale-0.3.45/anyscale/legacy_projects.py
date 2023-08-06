import copy
from typing import Any, Dict, Optional

import click


def format_command(command: str, parsed_args: Dict[Any, Any]) -> str:
    """Substitute arguments into command.
    Args:
        command (str): Shell comand with argument placeholders.
        parsed_args (dict): Dictionary that maps from argument names
            to their value.
    Returns:
        Shell command with parameters from parsed_args substituted.
    """
    for key, val in parsed_args.items():
        command = command.replace("{{" + key + "}}", str(val))
    return command


def get_session_runs(
    name: Optional[str], command: Optional[str], parsed_args: Dict[Any, Any]
) -> Any:
    """Get a list of sessions to start.
    Args:
        command (str): Shell command with argument placeholders.
        parsed_args (dict): Dictionary that maps from argument names
            to their values.
    Returns:
        List of sessions to start, which are dictionaries with keys:
            "name": Name of the session to start,
            "command": Command to run after starting the session,
            "params": Parameters for this run,
            "num_steps": 4 if a command should be run, 3 if not.
    """
    if not command:
        return [{"name": name, "command": None, "params": {}, "num_steps": 3}]

    # Try to find a wildcard argument (i.e. one that has a list of values)
    # and give an error if there is more than one (currently unsupported).
    wildcard_arg = None
    for key, val in parsed_args.items():
        if isinstance(val, list):
            if not wildcard_arg:
                wildcard_arg = key
            else:
                raise click.ClickException(
                    "More than one wildcard is not supported at the moment"
                )

    if not wildcard_arg:
        session_run = {
            "name": name,
            "command": format_command(command, parsed_args),
            "params": parsed_args,
            "num_steps": 4,
        }
        return [session_run]
    else:
        session_runs = []
        for val in parsed_args[wildcard_arg]:
            parsed_args = copy.deepcopy(parsed_args)
            parsed_args[wildcard_arg] = val
            session_run = {
                "name": "{}-{}-{}".format(name, wildcard_arg, val),
                "command": format_command(command, parsed_args),
                "params": parsed_args,
                "num_steps": 4,
            }
            session_runs.append(session_run)
        return session_runs
