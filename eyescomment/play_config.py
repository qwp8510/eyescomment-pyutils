from config import Config
from os import path


CURRENT_PATH = path.dirname(path.abspath(__file__))

Config.set_dir(r'C:\Users\a4793\eyescomment-pyutils\tests\config.json')
print(Config.instance().get('PORTAL_SERVER'))
