"""
This file is used to trigger lambda functions locally and test
the results of the app on actual data to make sure of the results.
An example to use this functionality is like the one shows on
'app_test.py' and then that file can run in command line.

Note: make sure you run your tests on QA environment.

== app_test.py file
# added the main directory as the first path
from os.path import dirname
import sys
parent = dirname(dirname(__file__))
sys.path.insert(0, parent)

if __name__ == '__main__':
    collections = ['collection_to_delete']
    app = AppTestRun(lambda_function.lambda_handler, collections)
    app.run()

> python app_test -a 16886 -d True
"""

import argparse
import os
from distutils.util import strtobool
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from worker.data.operations import delete_collection_data_of_asset_id, get_one_data_record, gather_data_for_period, \
    point_main_envs
from worker.state.mixins import StateMixin
from worker.test.utils import get_last_processed_timestamp, create_scheduler_events


load_dotenv(override=True)


def generate_runner_parser():
    """
    Creating the supporting arguments
    :return:
    """
    parser = argparse.ArgumentParser(description="Run your tests on an asset.")
    parser.add_argument("-v", "--environment", "--env", type=str, required=False,
                        help="environment, options: 'local', 'qa', 'staging', 'production'")
    parser.add_argument("-a", "--asset_id", "--id", type=int, required=True,
                        help="set asset_id")
    parser.add_argument("-s", "--start_timestamp", "--start", type=int, required=False, default=None,
                        help="start timestamp")
    parser.add_argument("-e", "--end_timestamp", "--end", type=int, required=False, default=None,
                        help="end timestamp")
    parser.add_argument("-i", "--timestep", "--step", type=int, required=False, default=60,
                        help="trigger the lambda function once every step")
    parser.add_argument("-d", "--to_delete", "--delete", type=strtobool, required=False, default=False,
                        help="to delete the state and data")
    parser.add_argument("-g", "--storage_type", "--storage", type=str, required=False, default="redis",
                        help="type of state storage, redis or mongo")
    return parser


class AppTestRun:
    def __init__(self, lambda_handler, collections: List[str], constants=None, args: List[str] = None):
        """
        :param lambda_handler: lambda handler function to run
        :param collections: collections to erase in case to_delete is on
        :param constants: constants module of the whole app, if there is only one app in the whole repository
        pass nothing and the code takes care of that
        :param args: arguments for the run
        """
        self.lambda_handler = lambda_handler
        self.collections = collections

        if not constants:
            from worker import constants

        self.constants = constants

        self.event_type = None
        self.progress = None

        if args is None:
            parser = generate_runner_parser()
            args = parser.parse_args()

        self.initialize(args)

    def initialize(self, args):
        environment = args.environment

        # directing main environment variables to the provided env: API_KEY, API_ROOT_URL, CACHE_URL
        point_main_envs(environment)

        asset_id = args.asset_id

        start_timestamp = args.start_timestamp
        end_timestamp = args.end_timestamp
        step = args.timestep
        self.event_type = self.constants.get('global.event-type')
        to_delete = args.to_delete

        # Setup state storage type environment
        state_storage_type = args.storage_type.lower()
        os.environ["STATE_STORAGE_TYPE"] = state_storage_type

        state_keys = construct_state_keys(self.constants, asset_id)

        if not start_timestamp:
            start_timestamp = get_one_data_record(asset_id, timestamp_sort=+1).get('timestamp')

        if not end_timestamp:
            end_timestamp = get_one_data_record(asset_id, timestamp_sort=-1).get('timestamp')

        if to_delete:
            delete_state_data_of_asset_id(asset_id, state_keys, state_storage_type=state_storage_type)
            delete_collection_data_of_asset_id(asset_id, self.collections)
            print(f"Deleted relevant {state_storage_type} states and collections for this asset!")

        start_timestamp = get_last_processed_timestamp(asset_id, state_keys[0], state_storage_type) or start_timestamp
        print(f"asset_id: {asset_id}, timestamp interval: [{start_timestamp}, {end_timestamp}]")

        events = create_scheduler_events(asset_id, start_timestamp, end_timestamp, step)

        self.progress = tqdm(events, ncols=150)

    def run(self):
        print("\nRunning the main module started ...")
        for event in self.progress:
            schedule_time = str(int(event[0][0]['schedule_start'] / 1000))
            if self.event_type == "wits_stream":
                wits = gather_data_for_period(
                    int(event[0][0]['asset_id']),
                    int(event[0][0]['schedule_start'] / 1000),
                    int(event[0][0]['schedule_end'] / 1000)
                )
                if not wits:
                    continue
                event = [wits]
            self.lambda_handler(event, None)
            self.progress.set_description(schedule_time)

        # Reset environment for other tests
        del os.environ["STATE_STORAGE_TYPE"]


def construct_state_keys(consts, asset_id: int) -> List[str]:
    """
    Get the constants dict of an app and construct the storage keys.
    Note: the first key is the global app key.
    :param consts: app constants module
    :param asset_id: well asset id
    :return: a list of storage keys
    """
    app_key = consts.get("global.app-key")
    module_keys = list(consts.get(app_key).keys())
    state_app = StateMixin()
    global_state_key = state_app.get_formatted_state_key(asset_id, app_key)

    module_state_keys = [
        state_app.get_formatted_state_key(asset_id, app_key, module)
        for module in module_keys
    ]

    return [global_state_key, *module_state_keys]


def delete_state_data_of_asset_id(asset_id: int, state_keys: List[str], state_storage_type=None):
    """
    Delete the state from given storage type
    :param asset_id:
    :param state_keys:
    :param state_storage_type:
    :return:
    """
    state_app = StateMixin(state_storage_type)
    state_app.delete_states(asset_id, state_keys)
