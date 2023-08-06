# flake8: noqa: E402

# added the main directory as the first path
import json
from os.path import dirname
import sys

parent = dirname(dirname(__file__))
sys.path.insert(0, parent)

from dotenv import load_dotenv

from testcase.app import app_lambda
from worker import API
from worker.test import AppTestRun
from worker.test.lambda_function_test_run import generate_runner_parser
from worker.test.local_testing.to_local_transfer import ToLocalTransfer, generate_transfer_parser


load_dotenv(override=True)


if __name__ == '__main__':
    # ========== INPUTS ========== #
    # Inputs for local data transfer app
    source_env = 'qa'
    source_asset_id = 37070404
    start_timestamp = 1502586000
    end_timestamp = 1502587000

    # you don't need to update the followings, the default ones are used.
    config_collections = []
    main_collections = []

    # INPUTS for runner
    timestep = 200
    to_delete = True
    storage_type = 'redis'

    collections = ['drilling-efficiency.mse']

    # ===== To Local Transfer Run ===== #
    parser = generate_transfer_parser()
    args = parser.parse_args([
        '--source_environment', source_env,
        '--source_asset_id', str(source_asset_id),
        '--config_collections', json.dumps(config_collections),
        '--main_collections', json.dumps(main_collections),
        '--start_timestamp', str(start_timestamp),
        '--end_timestamp', str(end_timestamp)
    ])
    mover = ToLocalTransfer(args)
    mover.run()

    # ===== Runner ===== #
    parser = generate_runner_parser()
    args = parser.parse_args([
        '--environment', 'local',
        '--asset_id', str(mover.local_asset_id),
        '--start_timestamp', str(start_timestamp),
        '--end_timestamp', str(end_timestamp),
        '--timestep', str(timestep),
        '--to_delete', str(to_delete),
        '--storage_type', storage_type
    ])

    def run():
        # loading of constants should happen here to avoid conflicts
        from testcase.app.app_constants import constants
        app = AppTestRun(app_lambda.lambda_handler, collections, constants, args=args)
        app.run()

    run()
    api = API()
    res = api.get(
        path="/v1/data/corva", collection='drilling-efficiency.mse',
        asset_id=mover.local_asset_id, sort="{timestamp: 1}", limit=1000
    )

    assert res.count > 10
