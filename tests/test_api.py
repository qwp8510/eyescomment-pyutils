import pytest
from os import path

from eyescomment.api import Login
from eyescomment.config import Config

CURRENT_PATH = path.dirname(path.abspath(__file__))


def valid_access_token(access_token):
    assert isinstance(access_token, str)
    assert len(access_token) > 0


def test_get_login_access_token():
    Config.set_dir(path.join(CURRENT_PATH, 'config.json'))
    login = Login(host=Config.instance().get('PORTAL_SERVER'), cache_path='/cache/path')
    access_token = login.login
    valid_access_token(access_token)
    assert login.url == path.join(login.host, 'Users/login')

