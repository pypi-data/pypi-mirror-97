import jwt
from datetime import datetime, timedelta
from openapi_client import ApiClient
from openapi_client import Configuration
from openapi_client import AuthApi
from openapi_client.models import Authenticate

from threedi_api_client.config import Config, EnvironConfig

# Get new token REFRESH_TIME_DELTA before it really expires.
REFRESH_TIME_DELTA = timedelta(hours=4).total_seconds()


def get_auth_token(username: str, password: str, api_host: str):
    api_client = ApiClient(
        Configuration(
            username=username,
            password=password,
            host=api_host
        )
    )
    auth = AuthApi(api_client)
    return auth.auth_token_create(Authenticate(username, password))


def is_token_usable(token: str) -> bool:
    if token is None:
        return False

    try:
        # Get payload without verifying signature,
        # does NOT validate claims (including exp)
        payload = jwt.decode(
            token,
            options={"verify_signature": False},
        )
    except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return False

    expiry_dt = datetime.utcfromtimestamp(payload["exp"])
    sec_left = (expiry_dt - datetime.utcnow()).total_seconds()
    return sec_left >= REFRESH_TIME_DELTA


def refresh_api_key(config: Configuration):
    """Refreshes the access key if its expired"""
    api_key = config.api_key.get("Authorization")
    if is_token_usable(api_key):
        return

    refresh_key = config.api_key['refresh']
    if is_token_usable(refresh_key):
        api_client = ApiClient(Configuration(config.host))
        auth = AuthApi(api_client)
        token = auth.auth_refresh_token_create(
            {"refresh": config.api_key['refresh']}
        )
    else:
        token = get_auth_token(config.username, config.password, config.host)
    config.api_key = {
        'Authorization': token.access,
        'refresh': token.refresh
    }


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
