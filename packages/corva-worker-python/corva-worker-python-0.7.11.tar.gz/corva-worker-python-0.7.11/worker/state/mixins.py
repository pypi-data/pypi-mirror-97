import os
from typing import List

from cached_property import cached_property

from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.state.enums import StateStorageType
from worker.state.handlers.mongo import MongoStateHandler
from worker.state.handlers.redis import RedisStateHandler


class StateMixin(LoggingMixin, RollbarMixin):

    def __init__(self, state_storage_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get from environment if not provided, default to redis
        if state_storage_type:
            self.state_storage_type = StateStorageType(state_storage_type)  # Raises error if not in StateStorageType enum
        else:
            self.state_storage_type = StateStorageType(os.getenv("STATE_STORAGE_TYPE", "redis").lower())

        self.state = {}

    @cached_property
    def state_handler(self):
        """
        Return the initialized state handler of the given type
        :return:
        """
        if self.state_storage_type == StateStorageType.REDIS:
            return RedisStateHandler()

        if self.state_storage_type == StateStorageType.MONGO:
            return MongoStateHandler()

    def load_state(self, state_key: [str, None] = None, auto_migrate: bool = False, raise_warnings: bool = False) -> dict:
        """
        Load the state from mongo or redis
        :param state_key:
        :param auto_migrate: Set to True if auto-migration from one state storage service to current is needed
        :param raise_warnings: Set to True if size limits warnings should be printed
        :return:
        """
        if not state_key:
            state_key = self.get_formatted_state_key(self.asset_id, self.app_key, self.module_key)

        state = self.state_handler.load_state(self.asset_id, state_key)

        # if auto_migrate key is not passed in, attempt to get from environment
        if not auto_migrate:
            auto_migrate = os.getenv("AUTO_MIGRATE_STATE", "false").lower() == "true"

        if not state and auto_migrate:
            state = self.state_handler.migrate_state(self.asset_id, state_key)
            self.info(self.asset_id, f"Migrated state storage to {self.state_storage_type.value}.")

        size_object = self.state_handler.check_state_size(self.asset_id, state, state_key, raise_warnings=raise_warnings)

        self.debug(self.asset_id, f"Retrieved state from {self.state_storage_type.value} of size {size_object} kb")
        self.state = state
        return state

    def save_state(self, state_key: [str, None] = None, timestamp: [int, None] = None, raise_warnings: bool = True) -> None:
        """
        Save the state to mongo or redis
        :param state_key:
        :param timestamp:
        :param raise_warnings: Set to True if size limits warnings should be printed
        :return:
        """
        if not state_key:
            state_key = self.get_formatted_state_key(self.asset_id, self.app_key, self.module_key)

        size_object = self.state_handler.check_state_size(self.asset_id, self.state, state_key, raise_warnings=raise_warnings)
        self.state_handler.save_state(self.asset_id, self.state, state_key, timestamp)
        self.debug(self.asset_id, f"Saved state to {self.state_storage_type.value} of size {size_object} kb")

    def delete_states(self, asset_id: int, state_keys: [List[str], str]):
        """
        Delete state for current module
        :param state_keys:
        :param asset_id:
        :return:
        """
        if not isinstance(state_keys, list):
            state_keys = [state_keys]

        self.state_handler.delete_states(asset_id, state_keys)
        self.debug(asset_id, f"Deleted state from {self.state_storage_type.value}.")

    @staticmethod
    def get_formatted_state_key(asset_id: int, app_key: str, module_key: [str, None] = None) -> str:
        """
        Returns the state key in Corva naming format
        :param asset_id:
        :param module_key:
        :param app_key:
        :return:
        """
        state_key = "corva/{0}.{1}".format(asset_id, app_key)

        if module_key:
            return "{0}.{1}".format(state_key, module_key)

        return state_key
