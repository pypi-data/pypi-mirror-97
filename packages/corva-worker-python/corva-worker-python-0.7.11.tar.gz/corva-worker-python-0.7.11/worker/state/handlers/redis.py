import json
import os
from typing import List

from cached_property import cached_property
import redis

from worker.state.enums import StateStorageType
from worker.state.handlers.__init__ import StateHandler


class RedisStateHandler(StateHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state_storage_type = StateStorageType.REDIS
        state_storage_limit_fatal = os.getenv("STATE_STORAGE_CRITICAL_LIMIT", 1_000.0)  # 1 MB
        state_storage_limit_warning = os.getenv("STATE_STORAGE_WARNING_LIMIT", 100.0)  # 100 kB
        self.set_size_limit("fatal", float(state_storage_limit_fatal))
        self.set_size_limit("warning", float(state_storage_limit_warning))

    @cached_property
    def redis_connection(self):
        """
        Setup redis and get connection
        :return:
        """
        cache_url = os.getenv("CACHE_URL", None)

        if not cache_url:
            raise Exception("redis key (CACHE_URL) not found in Environment Variables.")
        _redis = redis.Redis.from_url(cache_url)

        if not _redis:
            raise Exception("Could not connect to Redis with URL: {cache_url}")

        return _redis

    def load_state(self, asset_id: int, state_key: str) -> dict:
        """
        Load state from redis
        :return:
        """
        state = self.redis_connection.get(state_key)
        if state:
            return json.loads(state)

        return {}

    def save_state(self, asset_id: int, state: dict, state_key: str, timestamp: [int, None]):
        """
        Save the state to redis
        :param asset_id:
        :param state:
        :param state_key:
        :param timestamp:
        :return:
        """
        self.redis_connection.set(state_key, value=json.dumps(state))

    def migrate_state(self, asset_id: int, state_key: str, from_state_storage=StateStorageType.MONGO) -> dict:
        """
        Attempt to get state from mongo and save it to redis
        This is needed for assets that already running, and saving state to redis
        Useful if the lambda has been setup for mongo but previous live assets are saving to redis
        :param asset_id:
        :param state_key:
        :param from_state_storage:
        :return:
        """
        if from_state_storage != StateStorageType.MONGO:
            return {}

        from worker.state.handlers.mongo import MongoStateHandler
        state_handler = MongoStateHandler()

        state = state_handler.load_state(asset_id, state_key)
        if not state:
            state = {}

        self.save_state(asset_id, state, state_key, None)
        return state

    def delete_states(self, asset_id: int, state_keys: List[str]):
        """
        Delete the states corresponding to given keys
        :param asset_id:
        :param state_keys: a list of redis keys
        :return:
        """
        self.redis_connection.delete(*state_keys)
