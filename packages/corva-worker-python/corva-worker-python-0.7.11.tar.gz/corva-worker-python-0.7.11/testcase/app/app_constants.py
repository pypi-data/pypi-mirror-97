import importlib
import worker
importlib.reload(worker)
from worker import constants  # noqa: #402


constants.update({
    "global": {
        "app-name": "WorkerTest-DrillingEfficiency",
        "app-key": "drilling-efficiency",
        "event-type": "scheduler",
        "query-limit": 3600,
    },
    "drilling-efficiency": {
        "mse": {
            "export-duration": 30,  # update and export results every 30 seconds
            "drilling-activity": ["Rotary Drilling", "Slide Drilling"],
            "required-channels": ['weight_on_bit', 'rotary_rpm', 'rotary_torque', 'rop'],
            "running-string": ["drillstring"],
            "reset-config": ["drillstring"]
        }
    }
})
