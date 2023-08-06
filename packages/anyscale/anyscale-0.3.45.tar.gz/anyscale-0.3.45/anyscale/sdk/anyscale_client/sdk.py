import anyscale.sdk.anyscale_client as anyscale_client
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi


class AnyscaleSDK(DefaultApi):  # type: ignore
    def __init__(self, auth_token: str, host: str = "https://beta.anyscale.com/ext"):
        configuration = anyscale_client.Configuration(host=host)
        configuration.connection_pool_maxsize = 100
        api_client = anyscale_client.ApiClient(
            configuration, cookie=f"cli_token={auth_token}"
        )

        super(AnyscaleSDK, self).__init__(api_client)
