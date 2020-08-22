import json


class Config():
    """ global config class"""

    _instance = None

    def __init__(self, config_dir=None):
        self.config_dir = config_dir

    @classmethod
    def instance(cls):
        if not cls._instance:
            with open(cls._config_dir) as js:
                cls._instance = json.load(js)
                js.close()
        return cls._instance

    @classmethod
    def set_dir(cls, config_dir):
        cls._config_dir = config_dir

    def dump(self, data):
        with open(self.config_dir, 'w') as js:
            json.dump(data, js)
            js.close()

    def read(self):
        with open(self.config_dir, 'r') as js:
            content = json.load(js)
            js.close()
        return content
