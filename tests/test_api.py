from os import path

from eyescomment.api import Login, Api
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


def test_api_get_access_token():
    Config.set_dir(path.join(CURRENT_PATH, 'config.json'))
    api = Api(
        host=Config.instance().get('PORTAL_SERVER'),
        target_path='Youtube_channels',
        cache_path=Config.instance().get('CACHE_DIR'))
    filter_params = {'where': {'channelId': 'UC6FcYHEm7SO1jpu5TKjNXEA'}}
    params = api.update_params_token(params=filter_params)
    assert isinstance(params, dict)
    assert params.get('where') == {'channelId': 'UC6FcYHEm7SO1jpu5TKjNXEA'}
    valid_access_token(params.get('access_token'))


def test_api_get():
    TGOP_channel_data = {
        "id": 1,
        "channelName": "這群人TGOP",
        "channelId": "UC6FcYHEm7SO1jpu5TKjNXEA",
        "location": "TW",
        "category": "Entertainment",
        "language": "Chinese_Traditional",
        "contact": "thisgroupofpeople@gmail.com",
        "createdAt": "2008-06-07T00:00:00.000Z",
        "updateLock": None,
        "subscriber": None
    }
    Config.set_dir(path.join(CURRENT_PATH, 'config.json'))
    api = Api(
        host=Config.instance().get('PORTAL_SERVER'),
        target_path='Youtube_channels',
        cache_path=Config.instance().get('CACHE_DIR'))
    filter_params = {'where': {'channelId': 'UC6FcYHEm7SO1jpu5TKjNXEA'}}
    channel_data = api.get(params=filter_params)
    assert isinstance(channel_data, list)
    assert channel_data[0] == TGOP_channel_data
