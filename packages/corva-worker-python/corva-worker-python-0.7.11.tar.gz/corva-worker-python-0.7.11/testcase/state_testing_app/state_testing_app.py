from testcase.state_testing_app.state_modules import TestRedis, TestMongo, TestMigration
from worker import App


class TestingApp(App):
    # override
    def get_modules(self):
        return [
            TestMongo,  # Mongo testing module
            TestRedis,  # Redis testing module
            TestMigration  # Migration from one state storage to another testing module
        ]

    def load(self, event):
        return
