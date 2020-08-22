import json
from ..api import Api


class RegionApi(Api):
    def __init__(self, host, target_path, cache_path):
        super(RegionApi, self).__init__(
            host=host, target_path=target_path, cache_path=cache_path
        )

    def get(self, params=None):
        data = super(RegionApi, self).get(
            params={"filter": json.dumps(params)})
        return data

    def push(self, data):
        super(RegionApi, self).post(json=data)
