import json


def get_json_content(dir):
    with open(dir, 'r') as js:
        content = json.load(js)
        js.close()
    return content

def dump_json_content(dir, data):
    with open(dir, 'w') as js:
        json.dump(data, js)
        js.close()
