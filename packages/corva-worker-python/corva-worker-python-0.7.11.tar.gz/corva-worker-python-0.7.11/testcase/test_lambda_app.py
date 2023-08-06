import unittest

from testcase.app.drilling_efficiency_app import DrillingEfficiency

from testcase.app.disable_module import DisableModule
from worker.test import AppTestRun
from worker import API
from worker.test.lambda_function_test_run import generate_runner_parser
from testcase.app import app_lambda


class TestLambdaApp(unittest.TestCase):

    def test_lambda_app(self):
        asset_id = 3083

        def run():
            # turning off the "AnotherModule" for the testing purpose
            DisableModule.enabled = False

            drilling_efficiency_app = DrillingEfficiency()
            active_modules = drilling_efficiency_app.get_active_modules()
            collections = [module.collection for module in active_modules]

            parser = generate_runner_parser()
            args = parser.parse_args([
                '--asset_id', str(asset_id),
                '--start_timestamp', '1502041854',
                '--end_timestamp', '1502043349',
                '--timestep', '600',
                '--to_delete', str(True),
                '--storage_type', str('mongo')
            ])

            # loading of constants should happen here to avoid conflicts
            from testcase.app.app_constants import constants
            app = AppTestRun(app_lambda.lambda_handler, collections, constants, args=args)
            app.run()

        try:
            run()

            api = API()
            records = api.get(
                path="/v1/data/corva", collection='drilling-efficiency.mse',
                asset_id=asset_id, sort="{timestamp: 1}", limit=1000,
            ).data

            self.assertEqual(42, len(records))
        except Exception:
            self.fail("This run should not fail.")
