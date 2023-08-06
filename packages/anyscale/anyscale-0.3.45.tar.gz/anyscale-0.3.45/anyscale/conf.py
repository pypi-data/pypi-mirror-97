import os
from typing import Optional

AWS_PROFILE = None

ANYSCALE_ENDPOINTS = {
    "development": "https://anyscale-dev.dev",
    "staging": "https://anyscale.dev",
    "production": "https://beta.anyscale.com",
    "test": "",
}

ANYSCALE_ENV = os.environ.get("DEPLOY_ENVIRONMENT", "production")
ANYSCALE_HOST = os.environ.get("ANYSCALE_HOST", ANYSCALE_ENDPOINTS[ANYSCALE_ENV])

# Global variable that contains the server session token.
CLI_TOKEN: Optional[str] = None

TEST_MODE = False
TEST_V2 = False

ANYSCALE_IAM_ROLE_NAME = "anyscale-iam-role"
ANYSCALE_AWS_SECURITY_GROUP_NAME = "anyscale-security-group"
