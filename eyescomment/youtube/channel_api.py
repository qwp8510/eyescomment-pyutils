import json

from ..api import OwnerApi


class ChannelApi(OwnerApi):
    def __init__(self, host, target_path, cache_path):
        super(ChannelApi, self).__init__(
            host=host, target_path=target_path, cache_path=cache_path
        )

    def get(self, params=None):
        data = super(ChannelApi, self).get(
            params={"filter": json.dumps(params)})
        return data

    def push(self, data):
        super(ChannelApi, self).post(json=data)
