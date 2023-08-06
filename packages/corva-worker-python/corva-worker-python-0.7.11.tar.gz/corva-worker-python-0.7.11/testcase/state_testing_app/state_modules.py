import os
import time

from worker import Module
from worker.app.modules.trigger import Trigger
from worker.state.enums import StateStorageType


class TestMongo(Module):
    module_key = "mongo-tester"
    collection = "None"

    module_state_fields = {
        'message': str,
    }

    # override
    def run_module(self, event, beginning_results):
        self.state_storage_type = StateStorageType.MONGO
        start_timer = time.time()
        reset_states(self)
        test_save_load(self)
        test_delete_states(self)
        self.state = {"message": f"This state is auto saved by module.run {self.module_key}"}
        print(f"Mongo tests completed in {int(time.time() - start_timer)} seconds.\n")

    def run(self, wits_stream: list):
        self.run_module(wits_stream, [])


class TestRedis(Module):
    module_key = "redis-tester"
    collection = "None"

    module_state_fields = {
        'message': str,
    }
    os.environ["STATE_STORAGE_TYPE"] = StateStorageType.REDIS.value

    # override
    def run_module(self, event, beginning_results):
        self.state_storage_type = StateStorageType.REDIS
        start_timer = time.time()
        reset_states(self)
        test_save_load(self)
        test_delete_states(self)
        self.state = {"message": f"This state is auto saved by module.run {self.module_key}"}
        print(f"Redis tests completed in {int(time.time() - start_timer)} seconds.\n")

    def run(self, wits_stream: list):
        self.run_module(wits_stream, [])


class TestMigration(Trigger):
    module_key = "migration-tester"
    collection = "None"

    module_state_fields = {
        'message': str,
    }

    # override
    def run_module(self, event, beginning_results):
        start_timer = time.time()
        global_state = {
            "asset_id": event.get("asset_id")
        }

        # Migration Tests
        print("Test auto migration of state")
        asset_id = global_state["asset_id"]
        module_key = self.module_key

        # Initialize and reset redis app
        redis_module = TestRedis(global_state, state_storage_type=StateStorageType.REDIS.value)
        redis_module.module_key = module_key
        redis_state_key = redis_module.get_formatted_state_key(global_state.get("asset_id"), redis_module.app_key, redis_module.module_key)
        redis_module.delete_states(asset_id, redis_state_key)
        redis_module.load_state(auto_migrate=False)

        # Initialize and reset mongo app
        mongo_module = TestMongo(global_state, state_storage_type=StateStorageType.MONGO.value)
        mongo_module.module_key = module_key
        mongo_state_key = mongo_module.get_formatted_state_key(global_state.get("asset_id"), mongo_module.app_key, mongo_module.module_key)
        mongo_module.delete_states(asset_id, mongo_state_key)
        mongo_module.load_state(auto_migrate=False)
        mongo_state = {"message": "This state is on mongo"}

        # Migration from mongo to redis
        # create a state on mongo
        # delete the state from redis
        # try to load from redis, it should automigrate from mongo to redis
        print("Test auto-migration from mongo to redis")
        mongo_module.state = mongo_state
        mongo_module.save_state()
        redis_module.delete_states(asset_id, redis_state_key)
        state = redis_module.load_state(auto_migrate=True)
        assert mongo_state == state

        # Initialize and reset redis app
        redis_module = TestRedis(global_state, state_storage_type=StateStorageType.REDIS.value)
        redis_module.module_key = module_key
        redis_module.delete_states(asset_id, redis_state_key)
        redis_module.load_state(auto_migrate=False)
        redis_state = {"message": "This state is on redis"}

        # Initialize and reset mongo app
        mongo_module = TestMongo(global_state, state_storage_type=StateStorageType.MONGO.value)
        mongo_module.module_key = module_key
        mongo_module.delete_states(asset_id, mongo_state_key)
        mongo_module.load_state(auto_migrate=False)

        # Migration from redis to mongo
        # create a state on redis
        # delete the state from mongo
        # try to load from mongo, it should automigrate from redis to mongo
        print("Test auto-migration from redis to mongo")
        redis_module.state = redis_state
        redis_module.save_state()
        mongo_module.delete_states(asset_id, mongo_state_key)
        state = mongo_module.load_state(auto_migrate=True)
        assert redis_state == state

        self.state = {"message": f"This state is auto saved by module.run {self.module_key}"}
        print(f"Migration tests completed in {int(time.time() - start_timer)} seconds.\n")


def test_delete_states(main_module):
    # Deletion Tests
    state_storage_type = main_module.state_storage_type.value
    print(f"Delete test for {state_storage_type}")

    asset_id = main_module.global_state["asset_id"]

    modules = []
    for i in range(5):
        _module_key = f"delete.test{i}"
        module = main_module.__class__(main_module.global_state, state_storage_type=state_storage_type)
        module.module_key = _module_key
        state_key = module.get_formatted_state_key(asset_id, module.app_key, _module_key)
        state = {"message": f"{module.state_storage_type.value} state {state_key}"}
        module.state = state
        module.save_state()
        modules.append(module)
        time.sleep(0.1)  # back-off to prevent blocking by redis/mongo

    # Delete Multiple
    state_keys = [
        main_module.get_formatted_state_key(asset_id, module.app_key, module.module_key)
        for module in modules
    ]
    multiple_state_keys = state_keys[0:4]

    main_module.delete_states(asset_id, multiple_state_keys)
    for i in range(4):
        _module_key = f"delete.test{i}"
        current_state = modules[i].load_state(auto_migrate=False)
        assert current_state == {"message": None}

    # Delete Single
    main_module.delete_states(asset_id, state_keys[4])
    current_state = modules[4].load_state(auto_migrate=False)
    assert current_state == {"message": None}


def reset_states(module):
    # Initialize and reset states
    print(f"Initialize test for {module.state_storage_type.value}")
    asset_id = module.global_state["asset_id"]
    state_key = module.get_formatted_state_key(asset_id, module.app_key, module.module_key)
    module.delete_states(asset_id, state_key)
    module.load_state()


def test_save_load(module):
    # Save/load tests
    print(f"Save/load test for {module.state_storage_type.value}")
    current_state = {"message": f"This state is on {module.state_storage_type.value}"}
    module.state = current_state
    module.save_state()
    state = module.load_state(auto_migrate=False)
    assert current_state == state
