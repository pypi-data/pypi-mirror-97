from openapi_client.aio.api_client import ApiClient
from openapi_client.aio.configuration import Configuration

from threedi_api_client.threedi_api_client import refresh_api_key
from threedi_api_client.config import Config, EnvironConfig


class ThreediApiClient:
    def __new__(cls, env_file=None, config=None):
        if env_file is not None:
            user_config = Config(env_file)
        elif config is not None:
            user_config = config
        else:
            user_config = EnvironConfig()

        configuration = Configuration(
            host=user_config.get("API_HOST"),
            username=user_config.get("API_USERNAME"),
            password=user_config.get("API_PASSWORD"),
            api_key={"Authorization": '', "refresh": ''},
            api_key_prefix={"Authorization": "Bearer"}
        )
        configuration.refresh_api_key_hook = refresh_api_key
        api_client = ApiClient(configuration)
        return api_client
