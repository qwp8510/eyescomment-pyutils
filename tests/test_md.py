from os import path

from eyescomment.md import Mongodb
from eyescomment.config import Config


CURRENT_PATH = path.dirname(path.abspath(__file__))


def test_get_md_data():
    Config.set_dir(path.join(CURRENT_PATH, 'config.json'))
    md = Mongodb(
        cluster_name='raw-comment-chinese',
        db_name='comment-chinese',
        collection_name='comment-UC6FcYHEm7SO1jpu5TKjNXEA')
    doc = list(md.get({'commentId': 'Ugw-4khRtnDqAAmdp1Z4AaABAg'}))
    assert len(doc) == 1
    assert isinstance(doc[0], dict)
    assert 'videoId' in doc[0]
    assert 'author' in doc[0]
    assert 'text' in doc[0]
