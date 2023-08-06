import json
import os
import unittest

from worker.data.activity import Activity
from worker.data.activity.activity_grouping import ActivityGrouping, ActivityGroup
from worker.data.serialization import obj2json, json2obj
from worker.data.wits import WITS


class TestActivity(unittest.TestCase):
    # Mapping of merging activities:
    # key: merging group name
    # value: list of constituent activities that can be merged
    ACTIVITY_MERGING_DICTIONARY = {
        Activity.RUN_IN_HOLE: [Activity.RUN_IN_HOLE, Activity.DRY_REAMING_DOWN],
        Activity.PULL_OUT_OF_HOLE: [
            Activity.PULL_OUT_OF_HOLE, Activity.WASHING_UP,
            Activity.DRY_REAMING_UP, Activity.REAMING_UP
        ],
        Activity.CIRCULATING: [
            Activity.ROTARY_DRILLING, Activity.SLIDE_DRILLING,
            Activity.WASHING_DOWN, Activity.REAMING_DOWN,
            Activity.STATIC_OFF_BOTTOM, Activity.CIRCULATING,
            Activity.DRY_ROTARY_OFF_BOTTOM, Activity.ROTARY_OFF_BOTTOM,
            Activity.STATIC_ON_BOTTOM, Activity.CIRCULATING_ON_BOTTOM,
            Activity.DRY_ROTARY_ON_BOTTOM, Activity.CIRCULATING_AND_ROTARY_ON_BOTTOM,
            Activity.IN_SLIPS, Activity.UNCLASSIFIED
        ]
    }

    def test_activity_setting(self):
        activity = Activity("Reaming Down")
        self.assertEqual(Activity.REAMING_DOWN, activity)
        self.assertTrue(activity.is_reaming())
        self.assertTrue(activity.is_pipe_moving())
        self.assertTrue(activity.is_pumping())
        self.assertTrue(activity.is_rotating())

        activity = Activity("Rotary Off Bottom")
        self.assertNotEqual(Activity.REAMING_DOWN, activity)
        self.assertEqual(Activity.ROTARY_OFF_BOTTOM, activity)
        self.assertEqual("Rotary Off Bottom", activity.value)
        self.assertNotEqual("Rotary Drilling", activity.value)
        self.assertFalse(activity.is_reaming())
        self.assertFalse(activity.is_pipe_moving())
        self.assertTrue(activity.is_pumping())
        self.assertTrue(activity.is_rotating())

        activity = Activity("Rotary Drilling")
        self.assertNotEqual(Activity.WASHING_DOWN, activity)
        self.assertEqual(Activity.ROTARY_DRILLING, activity)
        self.assertEqual("Rotary Drilling", activity.value)
        self.assertFalse(activity.is_reaming())
        self.assertTrue(activity.is_pipe_moving())
        self.assertTrue(activity.is_pumping())
        self.assertTrue(activity.is_rotating())

    def test_activity_grouping(self):
        wits_records = get_data_for_activity_grouping()
        self.assertEqual(1714, len(wits_records))
        activity_grouping = ActivityGrouping(min_group_duration=5)
        groups = activity_grouping.group(wits_records)
        print()
        print("\n".join(str(grp) for grp in groups))
        self.assertEqual(18, len(groups))
        # the index of the groups and their expected results
        expected = {
            0: ActivityGroup(Activity('In Slips'), 1594037326, 1594037418),
            1: ActivityGroup(Activity('Static Off Bottom'), 1594037422, 1594037443),
            16: ActivityGroup(Activity('Rotary Off Bottom'), 1594038755, 1594038891),
            17: ActivityGroup(Activity('Rotary Drilling'), 1594038893, 1594039039)
        }
        for index, activity_group in expected.items():
            self.assertEqual(groups[index], activity_group)

    def test_activity_grouping_with_merging(self):
        wits_records = get_data_for_activity_grouping()

        self.assertEqual(1714, len(wits_records))

        activity_grouping = ActivityGrouping(min_group_duration=5, merging_dict=self.ACTIVITY_MERGING_DICTIONARY)
        groups = activity_grouping.group(wits_records)
        print()
        print("\n".join(str(grp) for grp in groups))
        # the index of the groups and their expected results
        expected = {
            0: ActivityGroup(Activity.CIRCULATING, 1594037326, 1594037418),
            1: ActivityGroup(Activity.CIRCULATING, 1594037422, 1594037443),
            2: ActivityGroup(Activity.RUN_IN_HOLE, 1594037444, 1594037541),
            3: ActivityGroup(Activity.CIRCULATING, 1594037542, 1594037646),
            4: ActivityGroup(Activity.RUN_IN_HOLE, 1594037650, 1594037800),
            5: ActivityGroup(Activity.CIRCULATING, 1594037801, 1594038017),
            6: ActivityGroup(Activity.CIRCULATING, 1594038022, 1594038582),
            7: ActivityGroup(Activity.CIRCULATING, 1594038586, 1594038751),
            8: ActivityGroup(Activity.CIRCULATING, 1594038755, 1594039039),
        }
        self.assertEqual(len(expected), len(groups))
        for index, activity_group in expected.items():
            self.assertEqual(groups[index], activity_group)

    def test_activity_serialization(self):
        washing_down = Activity.WASHING_DOWN
        ser = obj2json(washing_down)
        washing_down2 = json2obj(ser)
        self.assertEqual(washing_down, washing_down2)

    def test_merging_inslips(self):
        activities = ['In Slips'] + ['Run In Hole'] * 4 + ['In Slips'] + ['Run In Hole'] * 6 + ['In Slips'] * 18
        timestamps = list(range(len(activities)))

        wits_data = []
        for index in timestamps:
            wits_json = {'data': {'entry_at': timestamps[index], 'state': activities[index]}}
            w = WITS(wits_json)
            wits_data.append(w)
        activity_grouper = ActivityGrouping(
            min_group_duration=7,
            merging_dict=self.ACTIVITY_MERGING_DICTIONARY
        )
        activity_groups = activity_grouper.group(wits_data)
        self.assertEqual(1, len(activity_groups))
        self.assertEqual(18, activity_groups[0].duration)

    def test_activity_group_overlap(self):
        group1 = ActivityGroup(Activity.WASHING_DOWN, start=1, end=10)
        group2 = ActivityGroup(Activity.WASHING_DOWN, start=5, end=15)
        group3 = ActivityGroup(Activity.WASHING_DOWN, start=20, end=23)

        self.assertTrue(ActivityGroup.has_overlap(group1, group2))
        self.assertFalse(ActivityGroup.has_overlap(group2, group3))


def get_data_for_activity_grouping():
    wits_chunk = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'resources', 'test', 'activity_grouping.data')
    )

    with open(wits_chunk, 'r') as file:
        lines = file.readlines()
        wits_records = [WITS(json.loads(r)) for r in lines]

    return wits_records
