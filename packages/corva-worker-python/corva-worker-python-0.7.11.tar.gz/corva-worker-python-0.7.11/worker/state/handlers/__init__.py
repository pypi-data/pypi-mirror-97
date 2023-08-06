import json
import sys
from typing import List

from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin


class StateHandler(RollbarMixin, LoggingMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size_limits = {}
        self.state_storage_type = None

    def load_state(self, asset_id: int, state_key: str) -> dict:
        raise NotImplementedError("load_state method must be implemented")

    def save_state(self, asset_id: int, state: dict, timestamp: [int, None], state_key: str) -> None:
        raise NotImplementedError("save_state method must be implemented")

    def check_state_size(self, asset_id, state, state_key, raise_warnings=True):
        """
        Check the size of the state dictionary and generate warnings if necessary
        :param asset_id:
        :param state:
        :param state_key:
        :param raise_warnings:
        :return:
        """
        size_object = sys.getsizeof(json.dumps(state)) / 1024

        if not raise_warnings:
            return size_object

        size_limit = self.size_limits["fatal"]
        if size_object > size_limit:
            message = f"State to {self.state_storage_type.value} of state_key {state_key} is of size {size_object} kb > {size_limit} kb."
            self.fatal(asset_id, message)
            self.track_message(message, level="critical")
            return size_object

        size_limit = self.size_limits["warning"]
        if size_object > size_limit:
            message = f"State to {self.state_storage_type.value} of state_key {state_key} is of size {size_object} kb > {size_limit} kb."
            self.warn(asset_id, message)
            return size_object

        return size_object

    def migrate_state(self, asset_id: int, state_key: str, from_state_storage) -> dict:
        raise NotImplementedError("migrate_state method is not implemented")

    def delete_states(self, asset_id: int, state_keys: List[str]):
        raise NotImplementedError("delete_states method is not implemented")

    def set_size_limit(self, limit_type: str, state_storage_limit: float):
        self.size_limits[limit_type] = state_storage_limit
