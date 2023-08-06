import copy
from datetime import datetime
import json
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, Optional, Tuple, Union

import click
from openapi_client.rest import ApiException  # type: ignore
import yaml

from anyscale import ANYSCALE_ENV
from anyscale.api import get_api_client
from anyscale.autosync_heartbeat import (
    get_working_dir_host_mount_location,
    managed_autosync_session,
    perform_autopush_synchronization,
    perform_sync,
)
from anyscale.client.openapi_client import (  # type: ignore
    ComputeTemplateConfig,
    CreateComputeTemplate,
    CreateSessionFromSnapshotOptions,
    Session,
    SessionFinishUpOptions,
    SessionState,
    SessionUpOptions,
    SetupInitializeSessionOptions,
    StopSessionOptions,
)
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.cloud import get_cloud_id_and_name
from anyscale.cluster_config import (
    _configure_min_max_workers,
    _update_file_mounts,
    configure_for_session,
    get_cluster_config,
)
from anyscale.project import (
    get_project_id,
    get_project_session,
    get_project_sessions,
    load_project_or_throw,
)
from anyscale.util import (
    canonicalize_remote_location,
    download_anyscale_wheel,
    format_api_exception,
    get_container_name,
    get_endpoint,
    get_working_dir,
    populate_session_args,
    slugify,
    validate_cluster_configuration,
    wait_for_head_node_start,
    wait_for_session_start,
)
from anyscale.utils.aws_credentials_util import (
    get_credentials_as_env_vars_from_cluster_config,
)
from anyscale.utils.env_utils import set_env


def get_head_node_ip(cluster_config: Union[Dict[str, Any], str]) -> Any:
    from ray.autoscaler.sdk import get_head_node_ip

    return get_head_node_ip(cluster_config)


def rsync(*args: Any, **kwargs: Any) -> None:
    from ray.autoscaler.sdk import rsync as ray_rsync

    ray_rsync(*args, **kwargs)


class SessionController:
    def __init__(self, api_client: Optional[DefaultApi] = None):
        if api_client is None:
            api_client = get_api_client()
        self.api_client = api_client

    def stop(
        self,
        session_name: Optional[str],
        terminate: bool,
        delete: bool,
        workers_only: bool,
        keep_min_workers: bool,
        skip_snapshot: bool = False,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        sessions = get_project_sessions(project_id, session_name, self.api_client)
        terminate = terminate or delete

        if not session_name and len(sessions) > 1:
            raise click.ClickException(
                "Multiple active sessions: {}\n"
                "Please specify the one you want to stop with --session-name.".format(
                    [session["name"] for session in sessions]
                )
            )

        for session in sessions:
            # Stop the session and mark it as stopped in the database.
            self.api_client.stop_session_api_v2_sessions_session_id_stop_post(
                session.id,
                StopSessionOptions(
                    terminate=terminate,
                    workers_only=workers_only,
                    keep_min_workers=keep_min_workers,
                    delete=delete,
                    take_snapshot=not skip_snapshot,
                ),
            )

        session_names = [session.name for session in sessions]
        session_names_str = ", ".join(session_names)
        url = get_endpoint(f"/projects/{project_id}")
        print(f"Session {session_names_str} stopping. View progress at {url}")

    def _load_cluster_config(
        self, config: Optional[str], session_exists: bool, project_definition: Any
    ) -> Optional[Dict[str, Any]]:
        """config option to cluster config.

        Excision of existing logic for C901.
        """
        cluster_config = None
        if not session_exists:
            config_attribute_provided = True
            if not config:
                config_attribute_provided = False
                config = project_definition.cluster_yaml()

            config = str(config)  # for typing.
            if not os.path.exists(config):
                if config_attribute_provided:
                    raise ValueError("Config file {} not found".format(config))
                else:
                    raise ValueError(
                        "No config param provided and default config file session-default.yaml not found. Please provide a config file using the --config attribute."
                    )

        if config:
            with open(config) as f:
                cluster_config_filled = populate_session_args(f.read(), config)
                cluster_config = yaml.safe_load(cluster_config_filled)

            validate_cluster_configuration(config, cluster_config, self.api_client)

        return cluster_config

    def up(
        self,
        session_name: Optional[str],
        config: Optional[str],
        build_id: Optional[str],
        compute_template_id: Optional[str],
        min_workers: Optional[int],
        max_workers: Optional[int],
        no_restart: bool,
        restart_only: bool,
        disable_sync: bool,
        cloud_id: Optional[str],
        cloud_name: Optional[str],
        idle_timeout: Optional[int],
        yes: bool,
        verbose: bool = False,
        no_rapid_start: bool = False,
    ) -> None:
        import ray.scripts.scripts as autoscaler_scripts

        # TODO(ilr) Split this into ~3 functions, look at jbai's comments on #1469

        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)

        if not session_name:
            session_name = str(
                self.api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(
                    project_id=project_id,
                ).result.name
            )

        session_list = self.api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, active_only=False, name=session_name
        ).results

        session_exists = len(session_list) > 0

        # Deduce whether we are launching this session
        # from a cluster config yaml
        # as opposed to a build ID + compute template ID combination.
        # The logic is:
        #  - If either build or compute template is specified,
        #    we will use those. Both must be specified.
        #  - Otherwise, we will use a cluster config yaml.
        #     - If a yaml name is explicitly specified, we will use that.
        #     - Otherwise, look for session-default.yaml.
        using_cluster_config = build_id is None and compute_template_id is None
        if not using_cluster_config:
            if config:
                raise ValueError(
                    "If launching from a build/compute template, a config file cannot be specified."
                )
            if not build_id or not compute_template_id:
                raise ValueError(
                    "Both build ID and Compute Template must be specified if launching a session that way."
                )

        # If using a user cluster config, load it.
        maybe_cluster_config = None
        if using_cluster_config:
            maybe_cluster_config = self._load_cluster_config(
                config=config,
                session_exists=session_exists,
                project_definition=project_definition,
            )

        if no_rapid_start:
            if not maybe_cluster_config:
                raise ValueError(
                    "Please specify a cluster config if using no_rapid_start."
                )
            maybe_cluster_config["provider"]["bypass_rapid_start"] = True

        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_id, cloud_name)
        assert cloud_id is not None, "Failed to get cloud."

        with format_api_exception(ApiException):
            up_response = self.api_client.session_up_api_v2_sessions_up_post(
                session_up_options=SessionUpOptions(
                    project_id=project_id,
                    name=session_name,
                    cluster_config={"config": json.dumps(maybe_cluster_config)}
                    if maybe_cluster_config
                    else None,
                    build_id=build_id,
                    compute_template_id=compute_template_id,
                    cloud_id=cloud_id,
                    idle_timeout=idle_timeout,
                )
            ).result
        session_id = up_response.session_id

        # Download & write anyscale wheel!
        download_anyscale_wheel(self.api_client, session_id)

        # Get previous head IP
        with format_api_exception(ApiException):
            ip_resp = self.api_client.get_session_api_v2_sessions_session_id_get(
                session_id
            )
        prev_head_ip = ip_resp.result.head_node_ip

        cluster_config = up_response.cluster_config

        if cluster_config["provider"].get("type") != "kubernetes":
            cluster_config = configure_for_session(
                session_id,
                project_definition.root,
                api_client=self.api_client,
                disable_project_sync=disable_sync,
                _DO_NOT_USE_RAY_UP_ONLY_cluster_config=cluster_config,
            )

        with tempfile.NamedTemporaryFile(mode="w") as config_file:
            renamed_config = copy.deepcopy(cluster_config)
            renamed_config["cluster_name"] = up_response.cluster_name
            json.dump(renamed_config, config_file)
            config_file.flush()
            try:
                # Use the bundled Autoscaler by directly calling the scripts file
                command = [
                    sys.executable,
                    autoscaler_scripts.__file__,
                    "up",
                    "-vvvv" if verbose else "",
                    config_file.name,
                    "--no-restart" if no_restart else "",
                    "--restart-only" if restart_only else "",
                    "--yes",
                ]
                command_lst = [c for c in command if c]
                if max_workers:
                    command_lst.extend(["--max-workers", f"{max_workers}"])
                if min_workers:
                    command_lst.extend(["--min-workers", f"{min_workers}"])

                # Set OS enviornment variables temporarily.
                aws_credentials = get_credentials_as_env_vars_from_cluster_config(
                    cluster_config
                )

                env = {
                    **ANYSCALE_ENV,
                    **aws_credentials,
                }

                proc = subprocess.Popen(
                    command_lst,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    env=env,
                )
                startup_log = []
                while proc.stdout:
                    line = proc.stdout.readline().decode()
                    if not line:
                        break
                    print(line, end="")
                    startup_log.append(line)
                startup_log_str = "".join(startup_log)
                proc.communicate()

                ray_up_succeeded = proc.returncode == 0

                curr_head_ip = get_head_node_ip(renamed_config)

                if curr_head_ip != prev_head_ip and ray_up_succeeded:
                    print("Setting up Jupyter lab, Ray dashboard, and autopush ...")

                self.api_client.session_finish_up_api_v2_sessions_session_id_finish_up_post(
                    session_id=session_id,
                    session_finish_up_options=SessionFinishUpOptions(
                        startup_log=startup_log_str,
                        new_session=curr_head_ip != prev_head_ip,
                        head_node_ip=curr_head_ip,
                        cluster_launch_errored=not ray_up_succeeded,
                    ),
                )
                # NOTE This call will raise an error if the session is in any of the following
                # states (StartupErrored/Stopped/Terminated).
                wait_for_session_start(project_id, session_name, self.api_client)
                url = get_endpoint(f"/projects/{project_id}")
                print(f"Session {session_name} started. View at {url}")
            except Exception as e:
                raise click.ClickException("{}\nSession startup failed.".format(e))

    def up_internal(
        self,
        session_name: Optional[str],
        config: Optional[str],
        build_id: Optional[str],
        compute_config: Optional[str],
        min_workers: Optional[int],
        max_workers: Optional[int],
        no_restart: bool,
        restart_only: bool,
        disable_sync: bool,
        cloud_id: Optional[str],
        cloud_name: Optional[str],
        idle_timeout: Optional[int],
        verbose: bool = False,
        no_rapid_start: bool = False,
    ) -> None:
        # TODO(ilr) Split this into ~3 functions, look at jbai's comments on #1469
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)

        if no_restart and restart_only:
            raise click.ClickException(
                "Cannot set both --restart-only and --no-restart at the same time."
            )

        if not session_name:
            session_name = str(
                self.api_client.get_project_default_session_name_api_v2_projects_project_id_default_session_name_get(
                    project_id=project_id,
                ).result.name
            )
        else:
            session_name = slugify(session_name)

        session_list = self.api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, active_only=False, name=session_name
        ).results

        session_exists = len(session_list) > 0

        # Old cluster config launch path.
        cluster_config = None
        if build_id is None and compute_config is None:
            if session_exists and not config:
                # Get cluster config stored in DB from existing session
                session = session_list[0]
                resp = self.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                    session.id
                )
                cluster_config = yaml.safe_load(resp.result.config_with_defaults)
            elif not session_exists and not config:
                # Get cluster config stored in DB from project
                resp = self.api_client.get_project_latest_cluster_config_api_v2_projects_project_id_latest_cluster_config_get(
                    project_id=project_id
                )
                cluster_config = yaml.safe_load(resp.result.config_with_defaults)
            else:
                # Get cluster config from `config` argument
                config = str(config)
                if not os.path.exists(config):
                    raise ValueError("Config file {} not found".format(config))
                with open(config) as f:
                    cluster_config_filled = populate_session_args(f.read(), config)
                    cluster_config = yaml.safe_load(cluster_config_filled)
                validate_cluster_configuration(config, cluster_config, self.api_client)

            cluster_config = _configure_min_max_workers(
                cluster_config, min_workers, max_workers
            )
            if no_rapid_start:
                cluster_config["provider"]["bypass_rapid_start"] = True

            if disable_sync:
                start_empty_head_node_only = False
                cluster_config["file_mounts"] = {}
            else:
                start_empty_head_node_only = True
                cluster_config = _update_file_mounts(
                    cluster_config, project_definition.root, self.api_client
                )

        # Build and compute template launch path.
        else:
            # Most of the logic is handled in the backend;
            # here, we just need to make sure any CLI options are compatible.
            if min_workers is not None or max_workers is not None:
                # These are invalid options for now;
                # later, we can add logic to add them to the compute template
                # when we figure out what the semantics of this option
                # with differing "available_node_types" are.
                raise click.ClickException(
                    "Cannot set --min-workers or --max-workers in CLI when using compute templates; please set directly in the compute template."
                )

        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_id, cloud_name)
        assert cloud_id is not None, "Failed to get cloud."

        # We could also set the default idle_timeout in the function signature,
        # but that would break backwards compatibility with older versions of
        # the product which do have an "--idle-timeout" field
        if idle_timeout is None:
            idle_timeout = 120

        # Register the compute config with Anyscale and get its ID.
        compute_template_id = None
        if compute_config:
            with open(compute_config, "r") as f:
                config_dict = json.load(f)
            config_object = ComputeTemplateConfig(**config_dict)
            created_template = self.api_client.create_compute_template_api_v2_compute_templates_post(
                create_compute_template=CreateComputeTemplate(
                    name="autogenerated-config-{}".format(datetime.now().isoformat()),
                    project_id=project_id,
                    config=config_object,
                )
            ).result
            compute_template_id = created_template.id

        try:
            with format_api_exception(ApiException):
                up_response = self.api_client.start_empty_session_api_v2_sessions_start_empty_session_post(
                    session_up_options=SessionUpOptions(
                        project_id=project_id,
                        name=session_name,
                        cluster_config={"config": json.dumps(cluster_config)}
                        if cluster_config
                        else None,
                        build_id=build_id,
                        compute_template_id=compute_template_id,
                        cloud_id=cloud_id,
                        idle_timeout=idle_timeout,
                        restart_only=restart_only,
                        no_restart=no_restart,
                        start_empty_head_node_only=start_empty_head_node_only,
                    )
                ).result
            session_id = up_response.session_id
            second_update_required = up_response.second_update_required
            wait_for_head_node_start(
                project_id, session_name, session_id, self.api_client
            )

            try:
                if not disable_sync:
                    # Push will sync project directory to working directory.
                    self.push(
                        session_name,
                        source=None,
                        target=None,
                        config=None,
                        all_nodes=False,
                    )
            except Exception as e:
                self.api_client.cancel_startup_api_v2_sessions_session_id_cancel_startup_post(
                    session_id=session_id
                )
                raise click.ClickException(
                    "{}\nSession startup failed while transferring files".format(e)
                )

            with format_api_exception(ApiException):
                self.api_client.setup_and_initialize_session_api_v2_sessions_session_id_setup_and_initialize_session_post(
                    session_id=session_id,
                    setup_initialize_session_options=SetupInitializeSessionOptions(
                        project_id=project_id,
                        cluster_config={"config": json.dumps(cluster_config)},
                        restart_only=restart_only,
                        no_restart=no_restart,
                        no_update=not second_update_required,
                    ),
                )

            wait_for_session_start(project_id, session_name, self.api_client)
            url = get_endpoint(f"/projects/{project_id}/sessions/{session_id}")
            print(f"Session {session_name} started. View at {url}")
        except KeyboardInterrupt:
            self.api_client.stop_session_api_v2_sessions_session_id_stop_post(
                session_id,
                StopSessionOptions(
                    terminate=True,
                    workers_only=False,
                    keep_min_workers=False,
                    delete=False,
                    take_snapshot=False,
                ),
            )
            raise click.ClickException(
                f"Terminating session {session_name} due to keyboard interrupt."
            )

    def fork_session(
        self,
        session_name: str,
        new_session_name: str,
        project_name: Optional[str] = None,
    ) -> str:
        source_session = self._resolve_session(session_name, project_name)
        if source_session.state == SessionState.RUNNING:
            print(
                "WARNING: Session is currently running, this may take several minutes."
            )

        project_url = get_endpoint(f"/projects/{source_session.project_id}")
        print(
            f"Forking session {session_name} into {new_session_name}. You can view its progress at {project_url}"
        )
        cloned_session = self._fork_session_internal(source_session, new_session_name)
        print(f"Session {session_name} forked.")

        wait_for_session_start(
            cloned_session.project_id, cloned_session.name, self.api_client
        )
        url = get_endpoint(
            f"/projects/{cloned_session.project_id}/sessions/{cloned_session.id}"
        )
        return f"Session {cloned_session.name} started. View at {url}"

    def ssh(self, session_name: str, ssh_option: Tuple[str]) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session = get_project_session(project_id, session_name, self.api_client)

        cluster_config = get_cluster_config(session_name, self.api_client)

        with format_api_exception(ApiException):
            head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
                session.id
            ).result.head_ip

        ssh_user = cluster_config["auth"]["ssh_user"]
        key_path = cluster_config["auth"]["ssh_private_key"]
        container_name = get_container_name(cluster_config)

        command = (
            ["ssh"]
            + list(ssh_option)
            + ["-tt", "-i", key_path]
            + ["{}@{}".format(ssh_user, head_ip)]
            + (
                [f"docker exec -it {container_name} sh -c 'which bash && bash || sh'"]
                if container_name
                else []
            )
        )

        subprocess.run(command)  # noqa: B1

    def autopush(
        self,
        session_name: Optional[str] = None,
        verbose: bool = False,
        delete: bool = False,
        ignore_errors: bool = False,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        print(f"Active project: {project_definition.root}\n")

        session = get_project_session(project_id, session_name, self.api_client)

        wait_for_session_start(project_id, session.name, self.api_client)

        cluster_config = get_cluster_config(session_name, self.api_client)

        rsync_exclude = cluster_config.get("rsync_exclude") or []
        rsync_filter = cluster_config.get("rsync_filter") or []

        with format_api_exception(ApiException):
            head_ip = self.api_client.get_session_head_ip_api_v2_sessions_session_id_head_ip_get(
                session.id
            ).result.head_ip
        ssh_user = cluster_config["auth"]["ssh_user"]
        ssh_private_key_path = cluster_config["auth"]["ssh_private_key"]

        ssh_command = [
            "ssh",
            "-o",
            "StrictHostKeyChecking=no",
            "-o",
            "UserKnownHostsFile={}".format(os.devnull),
            "-o",
            "LogLevel=ERROR",
            "-i",
            ssh_private_key_path,
        ]
        source = project_definition.root
        target = get_working_dir(cluster_config, project_id, self.api_client)
        if bool(get_container_name(cluster_config)):
            target = get_working_dir_host_mount_location(
                ssh_command,
                ssh_user,
                head_ip,
                get_container_name(cluster_config),
                target,
            )

        print("Autopush with session {} is starting up...".format(session.name))
        with managed_autosync_session(session.id, self.api_client):
            # Performing initial full synchronization with rsync.
            first_sync = perform_sync(
                ssh_command,
                source,
                ssh_user,
                head_ip,
                target,
                delete,
                rsync_filter=rsync_filter,
                rsync_exclude=rsync_exclude,
            )  # noqa: B1

            if first_sync.returncode != 0:
                message = f"First sync failed with error code: {first_sync.returncode}."
                if ignore_errors:
                    print(
                        f'{message} Continuing to sync due to "--ignore-error" option.'
                    )
                else:
                    raise click.ClickException(
                        f"{message} If you would like to continue syncing, please use "
                        'autopush with "--ignore-error" option.'
                    )

            perform_autopush_synchronization(
                ssh_command,
                source,
                ssh_user,
                head_ip,
                target,
                delete=delete,
                rsync_filter=rsync_filter,
                rsync_exclude=rsync_exclude,
            )

    def pull(
        self,
        session_name: Optional[str] = None,
        source: Optional[str] = None,
        target: Optional[str] = None,
        config: Optional[str] = None,
    ) -> None:
        project_definition = load_project_or_throw()

        try:
            print("Collecting files from remote.")
            project_id = get_project_id(project_definition.root)
            cluster_config = get_cluster_config(session_name, self.api_client)
            directory_name = get_working_dir(
                cluster_config, project_id, self.api_client
            )
            source_directory = f"{directory_name}/"

            aws_credentials = get_credentials_as_env_vars_from_cluster_config(
                cluster_config
            )

            source = canonicalize_remote_location(cluster_config, source, project_id)

            with set_env(**aws_credentials):
                if source and target:
                    rsync(
                        cluster_config, source=source, target=target, down=True,
                    )
                elif source or target:
                    raise click.ClickException(
                        "Source and target are not both specified. Please either specify both or neither."
                    )
                else:
                    rsync(
                        cluster_config,
                        source=source_directory,
                        target=project_definition.root,
                        down=True,
                    )

            if config:
                session = get_project_session(project_id, session_name, self.api_client)
                with format_api_exception(ApiException):
                    resp = self.api_client.get_session_cluster_config_api_v2_sessions_session_id_cluster_config_get(
                        session.id
                    )
                cluster_config = yaml.safe_load(resp.result.config_with_defaults)
                with open(config, "w") as f:
                    yaml.dump(cluster_config, f, default_flow_style=False)

            print("Pull completed.")

        except Exception as e:
            print(e)
            raise click.ClickException(e)  # type: ignore

    def push(
        self,
        session_name: str,
        source: Optional[str],
        target: Optional[str],
        config: Optional[str],
        all_nodes: bool,
    ) -> None:
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)
        session = get_project_session(project_id, session_name, self.api_client)
        session_name = session.name

        cluster_config = get_cluster_config(session_name, self.api_client)
        target = canonicalize_remote_location(cluster_config, target, project_id)

        aws_credentials = get_credentials_as_env_vars_from_cluster_config(
            cluster_config
        )

        with set_env(**aws_credentials):
            if source and target:
                rsync(
                    cluster_config, source=source, target=target, down=False,
                )
            elif source or target:
                raise click.ClickException(
                    "Source and target are not both specified. Please either specify both or neither."
                )
            else:
                rsync(
                    cluster_config, source=None, target=None, down=False,
                )

        if config:
            validate_cluster_configuration(config, api_instance=self.api_client)
            print("Updating session with {}".format(config))
            self.up(
                session_name=session_name,
                config=None,
                build_id=None,
                compute_template_id=None,
                min_workers=None,
                max_workers=None,
                no_restart=False,
                restart_only=False,
                disable_sync=True,
                cloud_id=session.cloud_id,
                cloud_name=None,
                idle_timeout=None,
                yes=True,
            )
        url = get_endpoint(f"/projects/{project_id}/sessions/{session.id}")
        print(f"Pushed to session {session_name}. View at {url}")

    # Helpers

    def _resolve_session(
        self, session_name: str, project_name: Optional[str] = None
    ) -> Session:
        """
        Resolves a session by name.
        This is distinct from  `anyscale.project.get_project_session` because:
        1. we rely on project names instead of ids
        2. we allow non-active sessions to be resolved

        Raises an exception if the session does not exist.

        Params
        session_name - name of the session
        project_name - optional project name that the session is in;
                       if absent, we use the workspace's project
        """
        if project_name:
            with format_api_exception(ApiException):
                projects = self.api_client.list_projects_api_v2_projects_get().results
            project = next(
                project for project in projects if project.name == project_name
            )
            project_id = project.id
        else:
            project_definition = load_project_or_throw()
            project_id = get_project_id(project_definition.root)

        with format_api_exception(ApiException):
            sessions_list = self.api_client.list_sessions_api_v2_sessions_get(
                project_id, name=session_name
            ).results

        if len(sessions_list) == 0:
            raise click.ClickException(
                f"No session found with name {session_name} in project {project_id}"
            )

        return sessions_list[0]

    def _fork_session_internal(
        self, source_session: Session, new_session_name: str
    ) -> Session:
        """
        Creates a clone of the source session.
        Raises an exception if cloning fails.

        Params
        source_session - session to clone
        new_session_name - name of the new session
        """
        with format_api_exception(ApiException):
            self.api_client.fork_session_api_v2_sessions_session_id_fork_post(
                session_id=source_session.id,
                create_session_from_snapshot_options=CreateSessionFromSnapshotOptions(
                    project_id=source_session.project_id, name=new_session_name
                ),
                # forking an active session can take up to 180s
                _request_timeout=300000,
            )

        with format_api_exception(ApiException):
            forked_sessions_list = self.api_client.list_sessions_api_v2_sessions_get(
                project_id=source_session.project_id, name=new_session_name
            ).results

        if len(forked_sessions_list) == 0:
            raise click.ClickException("Unable to fork session.")

        return forked_sessions_list[0]
