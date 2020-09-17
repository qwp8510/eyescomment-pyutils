import pymongo
import logging
from os import path
from requests import Timeout

from .config import Config


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))


class Mongodb():
    collection_mapping = {}

    def __init__(self, cluster_name, db_name, collection_name):
        self.mongo_server = \
            'mongodb+srv://{}:{}@{}-erjue.gcp.mongodb.net/test?\
            retryWrites=true&w=majority'
        self.cluster_name = cluster_name
        self.db_name = db_name
        self.collection_name = collection_name
        self.db = self._db()

    def _db(self):
        try:
            config = Config.instance()
            cluster = self.mongo_server.format(
                config.get('MD_USERNAME'),
                config.get('MD_PASSWORD'),
                self.cluster_name
            )
            return pymongo.MongoClient(cluster)[self.db_name]
        except Timeout:
            logger.error('connect Mongodb with {} {} fail'.format(
                self.cluster_name, self.db_name))
        except Exception as e:
            logger.error('fail in _db: {}'.format(e))

    @property
    def _collection(self):
        self.collection_mapping.setdefault(
            self.collection_name, self.db[self.collection_name])

        return self.collection_mapping.get(self.collection_name)

    def get(self, filter_params={}):
        results = self._collection.find(filter_params)
        return results

    def insert_one(self, post_message):
        try:
            self._collection.insert_one(post_message)
        except Exception as e:
            logger.warning("insert {} to {} collection fail: {}".format(
                post_message, self.collection_name, e))

    def insert_many(self, post_messages):
        """
            insert format: [{ }, { }, ...]
        """
        try:
            self._collection.insert_many(post_messages)
        except Exception as e:
            logger.warning("insert_many {} to {} collection fail: {}".format(
                post_messages, self.collection_name, e))

    def delete_one(self, deleteMessage):
        try:
            logger.warning('deleting deleteMessage')
            self._collection.delete_one(deleteMessage)
        except Exception as e:
            logger.warning('delete {} to {} collection fail: {}'.format(
                deleteMessage, self.collection_name, e))

    def update_one(self, updateMessage):
        try:
            self._collection.update_one(updateMessage)
        except Exception as e:
            logger.warning("update {} to {} collection fail: {}".format(
                updateMessage, self.collection_name, e))
