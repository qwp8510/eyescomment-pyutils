import json


class Config():
    def __init__(self, Dir):
        self.configDir = Dir

    @property
    def content(self):
        with open(self.configDir) as js:
            f = json.load(js)
            js.close()
        return f

    def set_config(self, data):
        with open(self.configDir, 'w') as js:
            json.dump(data, js)
            js.close()
