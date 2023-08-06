"""
The purpose of this App is to test the StateMixin functionality
This app tests saving/loading, deleting and migration of states on two different storage types:
1. Mongo `temporary-state` collection
2. Redis
"""
from testcase.app.app_constants import constants  # noqa: F401
