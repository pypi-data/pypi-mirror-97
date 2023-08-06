# flake8: noqa: E402

"""
This test is created to make sure the framework for local testing
is working correctly.
"""

# added the main directory as the first path
from os.path import dirname
import sys

parent = dirname(dirname(__file__))
sys.path.insert(0, parent)

from testcase.app.disable_module import DisableModule
from testcase.app.drilling_efficiency_app import DrillingEfficiency
from testcase.app import app_lambda
from worker.test import AppTestRun


if __name__ == '__main__':

    # turning off the "AnotherModule" for the testing purpose
    DisableModule.enabled = False

    drilling_efficiency_app = DrillingEfficiency()
    active_modules = drilling_efficiency_app.get_active_modules()

    collections = [module.collection for module in active_modules]

    # loading of constants should happen here to avoid conflicts
    from testcase.app.app_constants import constants

    app = AppTestRun(app_lambda.lambda_handler, collections, constants)
    app.run()
