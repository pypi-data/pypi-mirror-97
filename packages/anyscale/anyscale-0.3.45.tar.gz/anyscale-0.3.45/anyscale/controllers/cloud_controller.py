"""
Fetches data required and formats output for `anyscale cloud` commands.
"""

import json
import os
from typing import Optional

import boto3
from click import ClickException
from openapi_client.rest import ApiException  # type: ignore

from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
from anyscale.client.openapi_client.models.cloud_config import CloudConfig  # type: ignore
from anyscale.client.openapi_client.models.write_cloud import WriteCloud  # type: ignore
from anyscale.cloud import get_cloud_id_and_name, get_cloud_json_from_id
import anyscale.conf
from anyscale.util import (
    _get_role,
    _resource,
    confirm,
    format_api_exception,
    get_available_regions,
    launch_gcp_cloud_setup,
)


class CloudController(object):
    def __init__(self, api_client: DefaultApi = None):
        if api_client is None:
            api_client = get_api_client()
        self.api_client = api_client

    def delete_cloud(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        skip_confirmation: bool,
    ) -> bool:
        """
        Deletes a cloud by name or id.
        """

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        confirm(
            f"You'll lose access to existing sessions created with cloud {cloud_id} if you drop it.\nContinue?",
            skip_confirmation,
        )

        with format_api_exception(ApiException):
            self.api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
                cloud_id=cloud_id
            )

        print(f"Deleted cloud {cloud_name}")

        return True

    def setup_cloud(self, provider: str, region: Optional[str], name: str) -> None:
        """
        Sets up a cloud provider
        """

        if provider == "aws":
            # If the region is blank, change it to the default for AWS.
            if region is None:
                region = "us-west-2"
            self.setup_aws(region=region, name=name)
        elif provider == "gcp":
            # If the region is blank, change it to the default for GCP.
            if region is None:
                region = "us-west1"
            # TODO: interactive setup process through the CLI?
            launch_gcp_cloud_setup(name=name, region=region)
        else:
            raise ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [aws, gcp]."
            )

    def setup_aws(self, region: str, name: str) -> None:
        from ray.autoscaler._private.aws.config import DEFAULT_RAY_IAM_ROLE

        os.environ["AWS_DEFAULT_REGION"] = region
        regions_available = get_available_regions()
        if region not in regions_available:
            raise ClickException(
                f"Region '{region}' is not available. Regions availables are {regions_available}"
            )

        confirm(
            "\nYou are about to give anyscale full access to EC2 and IAM in your AWS account.\n\n"
            "Continue?",
            False,
        )

        with format_api_exception(ApiException):
            user_info = self.api_client.get_user_info_api_v2_userinfo_get().result

        self.setup_aws_cross_account_role(region, user_info.id, name)
        self.setup_aws_ray_role(region, DEFAULT_RAY_IAM_ROLE)

        print("AWS credentials setup complete!")
        print(
            "You can revoke the access at any time by deleting anyscale IAM user/role in your account."
        )
        print("Head over to the web UI to create new sessions in your AWS account!")

    def setup_aws_cross_account_role(
        self, region: str, user_id: str, name: str
    ) -> None:
        with format_api_exception(ApiException):
            response = (
                self.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get()
            )

        anyscale_aws_account = response.result.anyscale_aws_account
        anyscale_aws_iam_role_policy = {
            "Version": "2012-10-17",
            "Statement": {
                "Sid": "1",
                "Effect": "Allow",
                "Principal": {"AWS": anyscale_aws_account},
                "Action": "sts:AssumeRole",
            },
        }

        role = _get_role(anyscale.conf.ANYSCALE_IAM_ROLE_NAME, region)

        if role is None:
            iam = _resource("iam", region)
            iam.create_role(
                RoleName=anyscale.conf.ANYSCALE_IAM_ROLE_NAME,
                AssumeRolePolicyDocument=json.dumps(anyscale_aws_iam_role_policy),
            )
            role = _get_role(anyscale.conf.ANYSCALE_IAM_ROLE_NAME, region)

        assert role is not None, "Failed to create IAM role!"

        role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess")
        role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/IAMFullAccess")

        print(f"Using IAM role {role.arn}")

        with format_api_exception(ApiException):
            self.api_client.create_cloud_api_v2_clouds_post(
                write_cloud=WriteCloud(
                    provider="AWS",
                    region=region,
                    credentials=role.arn,
                    creator_id=user_id,
                    name=name,
                )
            )

    def setup_aws_ray_role(self, region: str, role_name: str) -> None:
        iam = boto3.resource("iam", region_name=region)

        role = _get_role(role_name, region)
        if role is None:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": {
                            "Effect": "Allow",
                            "Principal": {"Service": ["ec2.amazonaws.com"]},
                            "Action": "sts:AssumeRole",
                        },
                    }
                ),
            )

            role = _get_role(role_name, region)

        # Default permissions (copied from upstream)
        role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/AmazonEC2FullAccess")
        role.attach_policy(PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess")

        # Also attach a role to allow it to launch more nodes with itself
        role.Policy("PassRoleToSelf").put(
            PolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PassRoleToSelf",
                            "Effect": "Allow",
                            "Action": "iam:PassRole",
                            "Resource": role.arn,
                        }
                    ],
                }
            )
        )

    def update_cloud_config(
        self,
        cloud_name: Optional[str],
        cloud_id: Optional[str],
        max_stopped_instances: int,
    ) -> None:
        """Updates a cloud's configuration by name or id.

        Currently the only supported option is "max_stopped_instances."
        """

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        with format_api_exception(ApiException):
            self.api_client.update_cloud_config_api_v2_clouds_cloud_id_config_put(
                cloud_id=cloud_id,
                cloud_config=CloudConfig(max_stopped_instances=max_stopped_instances),
            )

        print(f"Updated config for cloud '{cloud_name}' to:")
        print(self.get_cloud_config(cloud_name=None, cloud_id=cloud_id))

    def get_cloud_config(
        self, cloud_name: Optional[str] = None, cloud_id: Optional[str] = None,
    ) -> str:
        """Get a cloud's current JSON configuration."""

        if not cloud_id and not cloud_name:
            raise ClickException("Must either provide the cloud name or cloud id.")

        cloud_id, cloud_name = get_cloud_id_and_name(
            self.api_client, cloud_id, cloud_name
        )

        return str(get_cloud_json_from_id(cloud_id, self.api_client)["config"])
