from alfa_sdk.common.session import Session
from alfa_sdk.common.stores import AuthStore


def create_session(*, alfa_env=None, cache_token=True):
    if alfa_env is None:
        session = Session()
    else:
        session = Session(alfa_env=alfa_env)

    token = session.auth.get_token()
    if cache_token:
        AuthStore.set_value("token", token, group="cache")

    return session

