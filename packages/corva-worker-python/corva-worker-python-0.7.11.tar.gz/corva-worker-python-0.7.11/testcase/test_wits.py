import json
import os
import unittest

from worker.data.activity import Activity
from worker.data.enums import DataStatus, ChannelStatus
from worker.data.operations import compute_time_step
from worker.data.wits import serialize, Channel, WITS
from worker.test.utils import file_to_json


class TestWits(unittest.TestCase):
    def test_set_wits(self):
        wits_sample = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'wits_class',
                                                   'wits_sample1.json'))
        wits_json_list = file_to_json(wits_sample)

        wits = WITS.set_wits(wits_json_list)
        self.assertIsInstance(wits, list)

        wits_json_record = wits_json_list[0]
        wits = WITS.set_wits(wits_json_record)
        self.assertIsInstance(wits, WITS)

        self.assertEqual(1588280468, wits.timestamp)
        self.assertEqual(1588280468, wits.entry_at)
        self.assertEqual(12989, wits.hole_depth)
        self.assertEqual(12981.8, wits.bit_depth)
        self.assertEqual(113.2, wits.block_height)
        self.assertEqual(190.8, wits.hook_load)
        self.assertEqual(31.5, wits.weight_on_bit)
        self.assertEqual(0, wits.rop)
        self.assertEqual(0.14, wits.rotary_rpm)
        self.assertEqual(0.01898, wits.rotary_torque)
        self.assertEqual(596.13, wits.mud_flow_in)
        self.assertEqual(22.3, wits.mud_flow_out_percent)
        self.assertEqual(5148.15, wits.standpipe_pressure)
        self.assertEqual(93.37, wits.diff_press)
        self.assertEqual(96.05, wits.pump_spm_1)
        self.assertEqual(96.28, wits.pump_spm_2)
        self.assertIsNone(wits.pump_spm_3)
        self.assertEqual(192.32999999999998, wits.pump_spm_total)
        self.assertIsNone(wits.active_pit_volume)
        self.assertEqual(Activity.WASHING_DOWN, wits.state)

        self.assertEqual(DataStatus.VALID, wits.hole_depth.status)

        setattr(wits, "pump_spm_3", Channel(90.0, DataStatus.MISSING))
        self.assertEqual(90.0, wits.pump_spm_3)
        self.assertEqual(DataStatus.MISSING, wits.pump_spm_3.status)

        # converting wits to json
        wits_dict = wits.get_as_dict()
        self.assertEqual(1588280468, wits_dict['timestamp'])
        wits_dict_data = wits_dict['data']
        self.assertEqual(1588280468, wits_dict_data['entry_at'])
        self.assertEqual(5148.15, wits_dict_data['standpipe_pressure'])
        self.assertEqual("Washing Down", wits_dict_data['state'])

        # Test Deep Copy
        copied_wits = WITS.set_wits(serialize(wits))
        self.assertTrue(wits.mud_flow_out_percent == copied_wits.mud_flow_out_percent == 22.3)

    def test_wits_range_validation(self):
        wits_sample = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'wits_class', 'wits_sample1.json')
        )
        wits_json_list = file_to_json(wits_sample)

        wits = WITS.set_wits(wits_json_list)
        self.assertIsInstance(wits, list)

        wits_json_record = wits_json_list[0]
        wits = WITS.set_wits(wits_json_record)
        self.assertIsInstance(wits, WITS)

        self.assertEqual(1588280468, wits.timestamp)
        # data qc and clipping
        wits.mud_flow_out_percent = -6
        channel_range_mapping = {
            'mud_flow_out_percent': {
                'range': [0, 100],
                'operation': 'clip'
            }
        }
        wits.validate_range(channel_range_mapping)
        self.assertEqual(0, wits.mud_flow_out_percent)

    def test_get_mud_flow_in_status(self):
        wits_sample = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'wits_class',
                                                   'wits_sample1.json'))
        wits_sample = file_to_json(wits_sample)[0]

        wits = WITS.set_wits(wits_sample)

        self.assertEqual(ChannelStatus.ON, wits.mud_flow_in_status(low_mud_flow_in_threshold=20))
        self.assertEqual(ChannelStatus.OFF, wits.mud_flow_in_status(low_mud_flow_in_threshold=800))

        wits.mud_flow_in = None
        self.assertEqual(ChannelStatus.MISSING, wits.mud_flow_in_status(low_mud_flow_in_threshold=800))

    def test_get_spm_status(self):
        wits_sample = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'wits_class',
                                                   'wits_sample1.json'))
        wits_sample = file_to_json(wits_sample)[0]
        wits = WITS.set_wits(wits_sample)

        self.assertEqual(ChannelStatus.ON, wits.spm_status(low_spm_threshold=20))
        self.assertEqual(ChannelStatus.OFF, wits.spm_status(low_spm_threshold=200))

        wits.pump_spm_1 = 0
        self.assertEqual(ChannelStatus.ON, wits.spm_status(low_spm_threshold=20))

        wits.pump_spm_1 = None
        wits.pump_spm_2 = None
        self.assertEqual(ChannelStatus.MISSING, wits.spm_status(low_spm_threshold=100))

        wits_sample = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'wits_class',
                                                   'wits_sample2.json'))
        wits_sample = file_to_json(wits_sample)[0]
        wits = WITS.set_wits(wits_sample)

        self.assertEqual(ChannelStatus.OFF, wits.spm_status(low_spm_threshold=20))

    def test_compute_time_step(self):
        """
        Computing the time step with two method:
        - a list of wits records in WITS object format
        - a list of wits records in json format
        :return:
        """
        wits_chunk = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'activity_grouping.data')
        )

        with open(wits_chunk, 'r') as file:
            lines = file.readlines()
            records_dict = [json.loads(record) for record in lines]
            records_wits = [WITS(json.loads(record)) for record in lines]

            timestep_dict = compute_time_step(records_dict)
            timestep_wits = compute_time_step(records_wits)

            self.assertEqual(1, timestep_dict)
            self.assertEqual(1, timestep_wits)
