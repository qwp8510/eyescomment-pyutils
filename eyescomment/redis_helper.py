from redis import Redis
import json


class RedisHelper():
    REDIS_TEMPLATE = 'video-{video_id}'

    def __init__(self, host='localhost', port=6379, db=0):
        """ Redis contructor

        Args:
            host(str): default localhost
            port(str): default 6379
            db(int): default 0

        """
        self.host = host
        self.port = port
        self.db = db
        self._redis = None

    @property
    def redis(self):
        """ Return Redis instance"""
        if not self._redis:
            self._redis = Redis(self.host, self.port, self.db)
        return self._redis

    def _get_key_name(self, key):
        return self.REDIS_TEMPLATE.format(video_id=key)

    def get(self, key):
        """ Return Redis value of key
        Args:
            key(str)

        """
        return self.redis.get(self._get_key_name(key))

    def delete(self, key):
        """ Return delete key
        Args:
            key(str)

        """
        self.redis.delete(self._get_key_name(key))

    def update(self, key, value):
        """ Redis set """
        self.redis.set(name=self._get_key_name(key), value=json.dumps(value, ensure_ascii=False))

    def get_list(self, key, start=0, end=-1):
        """ Return Redis list value of key

        Args:
            key(str)
            start(int): start index
            end(int): end index

        """
        return self.redis.lrange(self._get_key_name(key), start, end)

    def update_list(self, key, value):
        """ Redis lpush """
        self.redis.lpush(self._get_key_name(key), json.dumps(value, ensure_ascii=False))
