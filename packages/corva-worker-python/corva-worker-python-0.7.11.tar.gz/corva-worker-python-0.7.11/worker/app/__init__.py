import json
import time
from typing import List

from worker.app.modules import Module

from worker.app.modules.time_activity_module import TimeActivityModule
from worker.data.operations import gather_data_for_period
from worker.framework import constants
from worker.mixins.logging import LoggingMixin
from worker.mixins.rollbar import RollbarMixin
from worker.state.mixins import StateMixin
from worker.state.state import State
from worker import exceptions


class App(StateMixin, LoggingMixin, RollbarMixin):
    app_state_fields = {
        'asset_id': int,
        'last_processed_timestamp': int
    }

    def __init__(self, *args, **kwargs):
        self.app_key = constants.get('global.app-key')
        self.app_name = constants.get('global.app-name')
        self.module_key = None

        state_storage_type = constants.get("global.state_storage_type", None)
        if state_storage_type is not None:
            # Add to kwargs if defined in constants, else will get from environment
            kwargs["state_storage_type"] = state_storage_type

        self.asset_id = None
        self.event = None

        super().__init__(*args, **kwargs)

    def load(self, event: str):
        """
        :param event: a scheduler event or wits stream
        :return:
        """
        event_type = self.get_event_type()
        valid_stream_collections = self.get_valid_stream_collections()
        event = self.clean_event(event)

        max_lookback_seconds = self.get_max_lookback_seconds()
        event = self.format_event(event_type, event)
        self.asset_id = self.determine_asset_id(event)

        self.state = self.load_state()

        event = self.load_event(event_type, event, max_lookback_seconds)
        self.event = self.filter_event_for_collections(event_type, valid_stream_collections, event)
        self.log_event(self.event, max_lookback_seconds)

    def log_event(self, event, max_lookback_seconds):
        self.debug(self.asset_id, "WITS input to {0} -> {1}".format(self.app_name, event))

        if not event:
            return

        batch_size = len(event)
        start_time = event[0].get("timestamp")
        end_time = event[-1].get("timestamp")
        system_time = time.time()

        self.debug(
            self.asset_id,
            "Received {} elements from {} to {} at {}. {} seconds of initial data are lookback.".format(
                batch_size, start_time, end_time, system_time, max_lookback_seconds
            )
        )

    @staticmethod
    def get_event_type():
        event_type = constants.get('global.event-type', "")

        if event_type not in ("scheduler", "wits_stream"):
            raise Exception('event_type specified incorrectly: {}'.format(event_type))

        return event_type

    @staticmethod
    def get_valid_stream_collections():
        valid_collections = constants.get('global.valid-stream-collections', [])
        if not isinstance(valid_collections, (str, list)):
            raise TypeError("Incorrect type of valid-stream-collections in global constants")

        if isinstance(valid_collections, str):
            valid_collections = [valid_collections]
        return valid_collections

    @staticmethod
    def clean_event(event):
        if not event:
            raise Exception("Empty event")

        try:
            if isinstance(event, (str, bytes, bytearray)):
                event = json.loads(event)
        except ValueError:
            raise Exception("Invalid event JSON")

        return event

    def get_max_lookback_seconds(self):
        """
        For each module (mostly in time-base modules), the time of processing does not
        match the last time of the event so extra data is required to look back and get
        the data so the processing can start from where it left off.
        :return:
        """

        time_modules = [module for module in self.get_modules() if issubclass(module, TimeActivityModule)]
        maximum_lookback = 0
        for module in time_modules:
            module_lookback = constants.get('{}.{}.export-duration'.format(self.app_key, module.module_key), default=0)
            maximum_lookback = max(module_lookback, maximum_lookback)

        return maximum_lookback

    def load_event(self, event_type, event, max_lookback_seconds):
        if event_type == 'scheduler':
            return self.load_scheduler_event(self.asset_id, event, max_lookback_seconds)

        if event_type == 'wits_stream':
            return self.load_wits_stream_event(self.asset_id, event, max_lookback_seconds)

        return None

    @staticmethod
    def filter_event_for_collections(event_type: str, valid_stream_collections: list, event: list):
        """
        This function filters the incoming event based on a list of valid collections

        :param event_type: Type of incoming event.
        :param valid_stream_collections: List of valid collections
        :param event: List of data records
        :return: List of records whose collection is one of the allowed event collections
        """

        # If event type is scheduler or event_collections is empty, return the entire event
        if event_type == 'scheduler' or not valid_stream_collections:
            return event

        # Filtering the event based on valid collections
        event = [record for record in event if record.get("collection") in valid_stream_collections]
        return event

    def filter_event_for_duplicates(self, event):
        last_processed_timestamp = self.state.get('last_processed_timestamp') or 0

        # If event is a single record and greater than the last processed timestamp, return the event
        if len(event) == 1 and event[0].get("timestamp") > last_processed_timestamp:
            return event

        # If length of unique timestamps is same as length of event and the first record timestamp is also greater than
        # last_processed_timestamp, then return the event
        unique_timestamps = set([record.get("timestamp") for record in event])
        if len(unique_timestamps) == len(event) and event[0].get("timestamp") > last_processed_timestamp:
            return event

        # Filtering the events for duplicates, once we identify that duplicates exist.
        filtered_events = []
        for each_record in event:
            if each_record.get("timestamp") > last_processed_timestamp:
                filtered_events.append(each_record)
                last_processed_timestamp = each_record.get("timestamp")

        return filtered_events

    def load_scheduler_event(self, asset_id, event, max_lookback_seconds):
        """
        To load a scheduler event and get the wits stream data
        :param asset_id: The asset to load
        :param event: The cleaned event from Kafka scheduler stream
        :param max_lookback_seconds: Maximum amount of time to look back prior to the scheduler event to cover gaps
        :return: list of WITS data between the last processed timestamp and the final event item timestamp
        """

        start_timestamp = self.state.get('last_processed_timestamp', event[0].get('timestamp') - 1)
        end_timestamp = event[-1].get('timestamp')

        # the event is converted from scheduler to wits stream
        scheduler_event = gather_data_for_period(
            asset_id=asset_id,
            start=start_timestamp - max_lookback_seconds,
            end=end_timestamp,
            limit=constants.get('global.query-limit'))

        return scheduler_event

    def load_wits_stream_event(self, asset_id, event, max_lookback_seconds):
        """
        To load a wits stream event and get more data if necessary
        :param asset_id: The asset to load
        :param event: The cleaned event from Kafka WITS stream
        :param max_lookback_seconds: Maximum amount of time to look back prior to WITS data to cover gaps
        :return: list of WITS data between the first event timestamp and the first timestamp
        """

        if event and max_lookback_seconds:
            # First filtering original event for duplicates
            event = self.filter_event_for_duplicates(event)

            first_timestamp = event[0].get('timestamp')

            if not first_timestamp:
                return event

            # Subtract one from the timestamp so that we don't reselect the final data item that was sent in the event
            end_timestamp = first_timestamp - 1

            previous_events = gather_data_for_period(
                asset_id=asset_id,
                start=first_timestamp - max_lookback_seconds,
                end=end_timestamp,
                limit=constants.get('global.query-limit'))

            event = previous_events + event

        return event

    @staticmethod
    def format_event(event_type: str, event: list) -> list:
        """
        validate the wits_stream event, flatten and organize the data into a desired format
        :param event_type: type of event
        :param event: a wits_stream event
        :return: a list of wits records
        """

        first_event = event[0]
        if isinstance(first_event, list):
            # This is possible for both scheduler and old wits stream event types
            try:
                # Because the events are structured into 'list of lists', using the following code
                # converts them into a flat single list. This is done for better data processing in
                # the proceeding steps.
                event = [item for sublist in event for item in sublist]
            except ValueError:
                raise Exception("Records are not valid JSON")

            if not isinstance(event, list):
                raise Exception("Records is not an array")

            if not event:
                raise Exception("Records is empty.")

            if event_type == 'scheduler':
                event = [
                    {
                        "asset_id": item["asset_id"],
                        "timestamp": int(item['schedule_start'] / 1000)
                    }
                    for item in event
                ]
            return event

        elif isinstance(first_event, dict):
            # This is possible for the new wits stream event type
            records = []
            for each in event:
                records = records + each.get("records", [])
            return records

        else:
            raise TypeError("Event is neither a scheduler, old nor new kafka consumer")

    @staticmethod
    def determine_asset_id(event: list) -> int:
        try:
            return int(event[0]["asset_id"])
        except Exception:
            raise Exception('Event does not contain asset_id: {}'.format(event))

    def load_state(self, state_key: [str, None] = None, auto_migrate: bool = False, raise_warnings: bool = False) -> dict:
        previous_state = super().load_state(state_key=state_key, auto_migrate=auto_migrate, raise_warnings=raise_warnings)

        state = State(self.app_state_fields, previous_state)

        if not state.get('asset_id', None):
            state['asset_id'] = self.asset_id

        return state

    def save_state(self, state_key: [str, None] = None, timestamp: [int, None] = None, raise_warnings: bool = True) -> None:
        if not timestamp:
            timestamp = self.state.get('last_processed_timestamp', 0)

        super().save_state(state_key=state_key, timestamp=timestamp, raise_warnings=raise_warnings)

    def get_modules(self) -> List[Module]:
        raise NotImplementedError("No modules found")

    def get_active_modules(self) -> List[Module]:
        return [module for module in self.get_modules() if module.enabled]

    def run_modules(self):
        if not self.event:
            return

        for module_type in self.get_active_modules():
            try:
                module = module_type(self.state, rollbar=self.rollbar)
            except Exception:
                raise exceptions.Misconfigured("Module {0} not able to initialize for asset_id {1}".format(module_type, self.asset_id))

            try:
                module.run(self.event)
            except Exception:
                message = f"Error in module {module_type.module_key}"
                self.track_error(message=message)
                raise

        last_processed_timestamp = self.event[-1].get('timestamp')
        self.state['last_processed_timestamp'] = last_processed_timestamp
