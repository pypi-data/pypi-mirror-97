import jwt
from threedi_api_client import ThreediApiClient
from datetime import datetime, timedelta, timezone
from threedi_api_client.threedi_api_client import (
    is_token_usable, REFRESH_TIME_DELTA)


SECRET_KEY = 'abcd1234'


def test_init_threedi_api_client_from_env_file(tmpdir):
    env_file = tmpdir / 'env_file'
    with open(str(env_file), 'w') as f:
        f.write("API_HOST=localhost:8000/v3.0\n")
        f.write("API_USERNAME=username\n")
        f.write("API_PASSWORD=password\n")
    ThreediApiClient(env_file=str(env_file))


def test_init_threedi_api_client_from_env_vars(monkeypatch):
    monkeypatch.setenv('API_HOST', 'localhost:8000/v3.0')
    monkeypatch.setenv('API_USERNAME', 'username')
    monkeypatch.setenv('API_PASSWORD', 'password')
    ThreediApiClient()


def test_init_threedi_api_client_from_config():
    config = {
        "API_HOST": "localhost:8000/v3.0",
        "API_USERNAME": "username",
        "API_PASSWORD": "password"
    }
    ThreediApiClient(config=config)


def get_token_with_expiry(delta_time: timedelta) -> int:
    utc_now = datetime.utcnow().replace(
        tzinfo=timezone.utc)
    exp = (utc_now + delta_time).replace(
        tzinfo=timezone.utc).timestamp()

    return jwt.encode(
        {
            'user': 'harry',
            'exp': exp
        },
        SECRET_KEY, algorithm='HS256'
    )


def test_not_expired_token():
    dt = timedelta(seconds=(REFRESH_TIME_DELTA + 10))
    assert is_token_usable(get_token_with_expiry(dt))


def test_expired_token():
    dt = timedelta(seconds=(REFRESH_TIME_DELTA - 10))
    assert not is_token_usable(get_token_with_expiry(dt))
