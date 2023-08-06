import json
import os
from typing import List

from cached_property import cached_property

from worker import API
from worker.state.enums import StateStorageType
from worker.state.handlers.__init__ import StateHandler


class MongoStateHandler(StateHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state_storage_type = StateStorageType.MONGO
        state_storage_limit_fatal = os.getenv("STATE_STORAGE_CRITICAL_LIMIT", 100_000.0)  # 100 MB
        state_storage_limit_warning = os.getenv("STATE_STORAGE_WARNING_LIMIT", 10_000.0)  # 10 MB
        self.set_size_limit("fatal", float(state_storage_limit_fatal))
        self.set_size_limit("warning", float(state_storage_limit_warning))

        self.api_path = "/v1/data/corva/temporary-state"

        self.created_timestamp = None
        self.mongo_id = None

    @cached_property
    def api(self):
        """
        Get the mongo/api connection setup
        :return:
        """
        return API()

    def load_state(self, asset_id: int, state_key: str) -> dict:
        """
        Load the state from mongo
        :param asset_id:
        :param state_key:
        :return:
        """
        query = "{state_key#eq#'%s'}" % state_key
        asset_id = asset_id
        sort = "{timestamp: -1}"
        state = self.api.get(path=self.api_path, asset_id=asset_id, sort=sort, query=query, limit=1).data

        if not state:
            return {}

        state = state[-1]
        self.mongo_id = state.get("_id")
        self.created_timestamp = state.get("timestamp")

        return state.get("data", {}).get("state", {})

    def save_state(self, asset_id: int, state: dict, state_key: str, timestamp: int):
        """
        Save the state to mongo
        :param asset_id:
        :param state:
        :param state_key:
        :param timestamp:
        :return:
        """
        state = {
            "state": state
        }
        record = {
            "collection": "temporary-state",
            "state_key": state_key,
            "updated_timestamp": timestamp,
            "version": 1,
            "provider": "corva",
            "asset_id": asset_id,
            "data": state,
        }

        if self.mongo_id:
            record["_id"] = self.mongo_id

        # if a blank state was loaded set the created timestamp to current timestamp
        record["timestamp"] = self.created_timestamp or timestamp
        response = self.api.post(path="/v1/data/corva", data=json.dumps(record)).data

        self.mongo_id = response.get("_id")
        return response

    def migrate_state(self, asset_id: int, state_key: str, from_state_storage=StateStorageType.REDIS) -> dict:
        """
        Attempt to get state from redis and save it to mongo
        This is needed for assets that already running, and saving state to redis
        Useful if the lambda has been setup for mongo but previous live assets were saving to redis
        :param asset_id:
        :param state_key:
        :param from_state_storage:
        :return:
        """
        if from_state_storage != StateStorageType.REDIS:
            return {}

        from worker.state.handlers.redis import RedisStateHandler
        state_handler = RedisStateHandler()

        state = state_handler.load_state(asset_id, state_key)

        created_timestamp = None
        if isinstance(state, dict):
            created_timestamp = state.get("timestamp") or state.get("last_processed_timestamp")

        if not state:
            state = {}

        self.save_state(asset_id, state, state_key, created_timestamp)
        return state

    def delete_states(self, asset_id: int, state_keys: List[str]):
        """
        Delete given state keys from mongo
        :param asset_id:
        :param state_keys:
        :return:
        """
        delete_count = 0
        for state_key in state_keys:
            delete_count += self._delete_state(asset_id, state_key)

        self.debug(asset_id, f"Deleted {delete_count} states")
        return delete_count

    def _delete_state(self, asset_id: int, state_key: str) -> int:
        """
        Delete state from mongo
        :param asset_id:
        :param state_key:
        :return:
        """
        query = "{asset_id#eq#%s}AND{state_key#eq#'%s'}" % (asset_id, state_key)
        response = self.api.delete(path=self.api_path, query=query)
        delete_count = response.data.get("deleted_count", 0)
        return delete_count
