import anyscale.client.openapi_client as openapi_client  # type: ignore
from anyscale.client.openapi_client.api.default_api import DefaultApi  # type: ignore
import anyscale.conf
from anyscale.credentials import load_credentials
import anyscale.sdk.anyscale_client as anyscale_client  # type: ignore
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi as AnyscaleApi  # type: ignore


def instantiate_api_client(
    no_cli_token: bool = False, cli_token: str = "", host: str = ""
) -> DefaultApi:
    """
    Instantiates client to interact with our frontend APIs
    """
    if (cli_token and not host) or (not cli_token and host):
        raise ValueError("Both cli_token and host need to be provided.")

    if not no_cli_token and anyscale.conf.CLI_TOKEN is None and not cli_token:
        anyscale.conf.CLI_TOKEN = load_credentials()
    configuration = openapi_client.Configuration(
        host=host or anyscale.conf.ANYSCALE_HOST
    )
    configuration.connection_pool_maxsize = 100

    if no_cli_token:
        api_client = openapi_client.ApiClient(configuration)
    else:
        cookie = (
            f"cli_token={cli_token}"
            if cli_token
            else f"cli_token={anyscale.conf.CLI_TOKEN}"
        )
        api_client = openapi_client.ApiClient(configuration, cookie=cookie)
    api_instance = openapi_client.DefaultApi(api_client)
    return api_instance


def instantiate_anyscale_client() -> AnyscaleApi:
    """
    Instantiates client to interact with our externalized APIs
    """

    if anyscale.conf.CLI_TOKEN is None:
        anyscale.conf.CLI_TOKEN = load_credentials()

    configuration = anyscale_client.Configuration(
        host=anyscale.conf.ANYSCALE_HOST + "/ext"
    )
    configuration.connection_pool_maxsize = 100

    api_client = anyscale_client.ApiClient(
        configuration, cookie=f"cli_token={anyscale.conf.CLI_TOKEN}"
    )

    api_instance = anyscale_client.DefaultApi(api_client)
    return api_instance


def get_api_client() -> DefaultApi:
    if _api_client.api_client is None:
        _api_client.api_client = instantiate_api_client()

    return _api_client.api_client


def get_anyscale_api_client() -> AnyscaleApi:
    if _api_client.anyscale_client is None:
        _api_client.anyscale_client = instantiate_anyscale_client()

    return _api_client.anyscale_client


class _ApiClient(object):
    api_client: DefaultApi = None
    anyscale_client: AnyscaleApi = None


_api_client = _ApiClient()
