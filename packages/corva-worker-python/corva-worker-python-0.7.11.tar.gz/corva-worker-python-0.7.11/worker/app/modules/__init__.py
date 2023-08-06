import json

from typing import Union

from worker.data.api import API
from worker.framework import constants
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.state.mixins import StateMixin

from worker.state.state import State


class Module(StateMixin, LoggingMixin, RollbarMixin):
    """
    This is an abstract base module that needs to be extended by an actual module.
    """
    # module_key is used for redis access and state of this module
    module_key = "module"
    collection = "collection"
    module_state_fields = {
        'last_processed_timestamp': int
    }

    enabled = True

    def __init__(self, global_state, *args, **kwargs):
        self.app_key = constants.get('global.app-key')
        self.app_name = constants.get('global.app-name')
        self.asset_id = global_state.get("asset_id")

        state_storage_type = constants.get("global.state_storage_type", None)
        if state_storage_type:
            kwargs["state_storage_type"] = state_storage_type

        self.global_state = global_state

        super().__init__(*args, **kwargs)

    def run(self, wits_stream: list):
        """
        :param wits_stream: a wits stream event
        :return:
        """
        # load the state
        state = self.load_state()
        self.state = self.process_module_state(state)

        # subclasses should implement their own run

    def should_run_processor(self, event):
        raise Exception("This method need to be implemented by subclasses!")

    def load_state(self, state_key: [str, None] = None, auto_migrate: bool = False, raise_warnings: bool = False) -> dict:
        current_state = super().load_state(state_key=state_key, auto_migrate=auto_migrate, raise_warnings=raise_warnings)
        return State(self.module_state_fields, current_state)

    @staticmethod
    def process_module_state(state):
        return state

    def set_state(self, key, value):
        self.state[key] = value

    def save_state(self, state_key: [str, None] = None, timestamp: [int, None] = None, raise_warnings: bool = True) -> None:
        if not timestamp:
            timestamp = self.global_state.get('last_processed_timestamp', 0)

        super().save_state(state_key=state_key, timestamp=timestamp, raise_warnings=raise_warnings)

    def load_dataset(self, event):
        return event

    def run_module(self, dataset: Union[list, dict], beginning_results: list) -> list:
        raise Exception("Not implemented")

    def get_last_exported_timestamp_from_collection(self, asset_id, query=None, less_than=None):
        """
        Query the module collection for this asset_id + module, sorted by timestamp descending,
        limit 1, grab the last item's timestamp. Default to 0 if no records found.
        @asset_id:
        @less_than: the timestamp before which you want to get
        """
        if less_than:
            query = query or ""
            query += "AND{timestamp#lt#%s}" % less_than

        worker = API()
        last_document = worker.get(
            path="/v1/data/corva", query=query, collection=self.collection, asset_id=asset_id,
            sort="{timestamp: -1}", limit=1,
        ).data

        if not last_document:
            return 0

        last_document = last_document[0]
        last_processed_timestamp = last_document.get('timestamp', 0)

        return last_processed_timestamp

    @staticmethod
    def gather_first_wits_timestamp_since(asset_id: int, since: int, activity_fields=None, operator='eq') -> int:
        """
        Query the Wits collection for this asset_id where state in wits_states and timestamp >= since
        """

        query = '{timestamp#%s#%s}' % ('gt', since)

        operator = operator.lower()

        if activity_fields:
            if operator == "eq" and isinstance(activity_fields, list):
                operator = "in"

            if operator in ("in", "nin"):
                if not isinstance(activity_fields, list):
                    activity_fields = [activity_fields]

                # Put each state into a formatted string for querying
                activity_fields = ["'{0}'".format(state) for state in activity_fields]
                activity_fields = "[{0}]".format(",".join(activity_fields))
            else:
                activity_fields = "'{0}'".format(activity_fields)

            query += 'AND{data.state#%s#%s}' % (operator, activity_fields)

        worker = API()
        first_wits_since = worker.get(
            path="/v1/data/corva", collection='wits', asset_id=asset_id, sort="{timestamp: 1}", limit=1, query=query
        ).data

        if not first_wits_since:
            return 0

        first_wits_since = first_wits_since[0]
        first_wits_since_timestamp = first_wits_since.get('timestamp', 0)

        return first_wits_since_timestamp

    @staticmethod
    def gather_maximum_timestamp(event, start, activity_fields):
        """
        get the maximum time stamp of a stream of data
        :param event: a stream of data  that the majority is wits collection
        :param start:
        :param activity_fields:
        :return:
        """
        maximum_timestamp = start
        for data in event:
            if data.get("collection") == "wits" and data.get('data', {}).get('state', None) in activity_fields:
                maximum_timestamp = max(data.get("timestamp", 0), maximum_timestamp)

        return maximum_timestamp

    def gather_minimum_timestamp(self, asset_id: int, event: list):
        minimum = self.get_last_exported_timestamp_from_collection(asset_id)

        if not minimum:
            minimum = event[0]["timestamp"] - 1800

        return minimum

    def gather_collections_for_period(self, asset_id, start, end, query=None):
        limit = constants.get("global.query-limit")

        query = query or ""
        if query:
            query += "AND"

        query += "{timestamp#gte#%s}AND{timestamp#lte#%s}" % (start, end)

        worker = API()
        dataset = worker.get(
            path="/v1/data/corva", collection=self.collection, asset_id=asset_id, query=query,
            sort="{timestamp: 1}", limit=limit,
        ).data

        if not dataset:
            return []

        return dataset

    def store_output(self, asset_id, output):
        """
        to store/post results
        :param asset_id: asset id of the well
        :param output: an array of json objects to be posted
        :return: None
        """

        if not asset_id or not output or not self.collection:
            return

        output = self.format_output(output)

        self.debug(asset_id, "{0} output -> {1}".format(self.module_key, output))

        worker = API()
        worker.post(path="/v1/data/corva", data=output)

    def build_empty_output(self, wits: dict) -> dict:
        """
        Building an empty output result.
        :param wits: one wits record
        :return:
        """
        output = {
            'timestamp': int(wits.get('timestamp')),
            'company_id': int(wits.get('company_id')),
            'asset_id': int(wits.get('asset_id')),
            'provider': str(wits.get('provider', 'corva')),
            'version': 1,
            'collection': self.collection,
            'data': {}
        }
        return output

    @staticmethod
    def format_output(output):
        output = json.dumps(output)
        return output
