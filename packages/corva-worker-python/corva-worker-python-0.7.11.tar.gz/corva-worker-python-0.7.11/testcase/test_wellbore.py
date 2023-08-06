import json
import os
import unittest

from worker import API
from worker.data.alert import Alerter
from worker.data.operations import get_data_by_path, get_one_data_record, get_config_by_id
from worker.data.serialization import obj2json, json2obj
from worker.mixins.logging import Logger
from worker.test.utils import file_to_json
from worker.wellbore.factory import run_drillstring_and_create_wellbore, run_casingstring_and_create_wellbore
from worker.wellbore.measured_depth_finder import get_unique_measured_depths
from worker.wellbore.model.annulus import Annulus
from worker.wellbore.model.drillstring import Drillstring
from worker.wellbore.model.enums import HoleType, PipeType
from worker.wellbore.model.hole import Hole
from worker.wellbore.model.hole_section import HoleSection


class TestSections(unittest.TestCase):
    def test_hole_section(self):
        hole_section1 = HoleSection(inner_diameter=5, top_depth=0, bottom_depth=20_000, hole_type=HoleType.OPEN_HOLE)

        hole_section1.set_length()

        self.assertEqual(20_000, hole_section1.length)

        expected_area = 19.634954084936208  # in INCH^2
        expected_volume = 2727.07695624114  # in FOOT^3

        self.assertAlmostEqual(expected_area, hole_section1.compute_get_area(), places=10)
        self.assertAlmostEqual(expected_volume, hole_section1.compute_get_volume(), places=10)

    def test_hole(self):
        casings = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "casings.json")
        )
        casings = file_to_json(casings)

        hole = Hole()
        hole.set_casings(casings)
        self.assertEqual(2, len(hole))

        hole_section1 = hole[0]
        self.assertAlmostEqual(6.88, hole_section1.inner_diameter, 10)
        self.assertAlmostEqual(6_770, hole_section1.length, 10)
        self.assertAlmostEqual(0, hole_section1.top_depth, 10)
        self.assertAlmostEqual(6_770, hole_section1.bottom_depth, 10)
        self.assertEqual(HoleType.CASED_HOLE, hole_section1.hole_type)

        hole_section2 = hole[1]
        self.assertAlmostEqual(4.67, hole_section2.inner_diameter, 10)
        self.assertAlmostEqual(14192, hole_section2.length, 10)
        self.assertAlmostEqual(6_770, hole_section2.top_depth, 10)
        self.assertAlmostEqual(20_962, hole_section2.bottom_depth, 10)
        self.assertEqual(HoleType.CASED_HOLE, hole_section2.hole_type)

        self.assertAlmostEqual(20_962, hole.get_bottom_depth(), 10)

        # Open hole
        open_hole = HoleSection(inner_diameter=4.5, top_depth=1111, bottom_depth=21_000, hole_type=HoleType.OPEN_HOLE)
        hole.add_section(open_hole)
        hole_section3 = hole[2]
        self.assertAlmostEqual(4.5, hole_section3.inner_diameter, 10)
        self.assertAlmostEqual(21_000 - 20_962, hole_section3.length, 10)
        self.assertAlmostEqual(20_962, hole_section3.top_depth, 10)
        self.assertAlmostEqual(21_000, hole_section3.bottom_depth, 10)
        self.assertEqual(HoleType.OPEN_HOLE, hole_section3.hole_type)

        self.assertAlmostEqual(21_000, hole.get_bottom_depth(), 10)

        # test fetching of the correct casing at a given depth
        casing1 = hole.find_section_at_measured_depth(10_000, False)
        self.assertEqual(id(hole_section2), id(casing1))

        # testing unique boundary depths
        mds = get_unique_measured_depths(hole)
        self.assertListEqual(mds, [0, 6770.0, 20962.0, 21000.0])

        # test serialization
        ser_str = obj2json(hole)
        hole_des = json2obj(ser_str)
        self.assertEqual(len(hole), len(hole_des))
        self.assertAlmostEqual(hole_des[1].inner_diameter, hole[1].inner_diameter, 10)
        self.assertAlmostEqual(hole_des[1].top_depth, hole[1].top_depth, 10)

        print("Hole:")
        print(hole)
        return hole

    def test_drillstring(self):
        drillstring_json_file = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "drillstring.json")
        )
        drillstring_json = file_to_json(drillstring_json_file)

        drillstring = Drillstring()
        drillstring.set_drillstring(drillstring_json)

        component_1 = drillstring[0]
        self.assertAlmostEqual(3.826, component_1.inner_diameter, 10)
        self.assertAlmostEqual(4.5, component_1.outer_diameter, 10)
        self.assertAlmostEqual(31, component_1.joint_length, 10)
        self.assertAlmostEqual(31, component_1.length, 10)

        component_6 = drillstring[5]
        self.assertAlmostEqual(2.75, component_6.inner_diameter, 10)
        self.assertAlmostEqual(4.75, component_6.outer_diameter, 10)
        self.assertAlmostEqual(29.09, component_6.joint_length, 10)
        self.assertAlmostEqual(29.09, component_6.length, 10)

        bit = drillstring[-1]
        self.assertAlmostEqual(6.75, bit.size, 10)
        self.assertAlmostEqual(1.1780972450961724, bit.tfa, 10)
        self.assertEqual(PipeType.BIT.value, bit.pipe_type.value, 10)

        # test for adjusting depths using bit depth
        wits = get_wits()
        drillstring.update(wits)
        self.assertAlmostEqual(wits.get('data', {}).get('bit_depth'), drillstring[-1].bottom_depth, 10)

        # test for finding drillstring section at a measured depth
        drillstring_section3 = drillstring.find_section_at_measured_depth(8_000, False)
        self.assertAlmostEqual(3.83, drillstring_section3.inner_diameter, 1)
        self.assertAlmostEqual(4.5, drillstring_section3.outer_diameter, 10)

        print("Drillstring")
        print(drillstring)
        return drillstring

    def test_annulus(self):
        drillstring = self.test_drillstring()
        hole = self.test_hole()
        annulus = Annulus(drillstring=drillstring, hole=hole)
        print("Annulus:")
        print(annulus)

        # 2nd DP should be split into two segments
        section2, section3 = annulus[2: 4]
        self.assertAlmostEqual(6.88, section2.inner_diameter_hole, 10)
        self.assertEqual(HoleType.CASED_HOLE, section2.hole_type)
        self.assertAlmostEqual(4.67, section3.inner_diameter_hole, 10)
        self.assertEqual(HoleType.CASED_HOLE, section3.hole_type)

        # the segment above the is extended to the bit depth
        last_section = annulus[-1]

        component_above_bit, bit = drillstring[-2:]
        combined_length = component_above_bit.length + bit.length

        self.assertAlmostEqual(combined_length, last_section.length, 10)

    def test_wellbore_creation_with_factory(self):
        """
        In this test case the creation of the wellbore through
        factory is shown; note that only the wits record is used
        and the other elements (casings, drillstrings) are fetched
        from the API.
        :return:
        """
        wits = get_wits()
        bit_depth = get_data_by_path(wits, 'data.bit_depth', float)
        hole_depth = get_data_by_path(wits, 'data.hole_depth', float)
        wellbore = run_drillstring_and_create_wellbore(wits)

        print("\n Hole configuration is:")
        hole = wellbore.actual_hole
        print(hole)
        self.assertEqual(2, len(hole))
        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertEqual(HoleType.OPEN_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(hole_depth, hole.get_bottom_depth(), 10)

        print("\n Drillstring configuration is:")
        drillstring = wellbore.actual_drillstring
        self.assertAlmostEqual(bit_depth, drillstring.bit_depth, 10)
        print(drillstring)

        print("\n Annulus configuration is:")
        annulus = wellbore.actual_annulus
        print(annulus)

        # testing drilling body volume change
        vol_change_calculated = wellbore.compute_get_drillstring_body_volume_change(6000, 5900)
        area_dp = wellbore.actual_drillstring[0].compute_body_cross_sectional_area_tj_adjusted()  # in INCH^2
        vol_expected = area_dp / 144 * -100
        self.assertAlmostEqual(vol_change_calculated, vol_expected, 10)

        # testing drilling outer solid volume change
        vol_change_calculated = wellbore.compute_get_drillstring_outside_volume_change(6000, 5900)
        area_dp = wellbore.actual_drillstring[0].compute_outer_area_tool_joint_adjusted()  # in INCH^2
        vol_expected = area_dp / 144 * -100
        self.assertAlmostEqual(vol_change_calculated, vol_expected, 10)

        # test serialization
        ser_str = obj2json(wellbore)
        wellbore_des = json2obj(ser_str)
        self.assertEqual(len(wellbore.actual_drillstring), len(wellbore_des.actual_drillstring))
        self.assertAlmostEqual(wellbore.actual_drillstring[1].inner_diameter, wellbore_des.actual_drillstring[1].inner_diameter, 10)
        self.assertAlmostEqual(wellbore.actual_drillstring[1].top_depth, wellbore_des.actual_drillstring[1].top_depth, 10)

    def test_wellbore_creation_with_under_reamer(self):
        """
        In this test case the creation of the wellbore through
        factory is shown; note that only the wits record is used
        and the other elements (casings, drillstrings) are fetched
        from the API.
        :return:
        """
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        asset_id = 81592982
        Logger.set_asset_id(asset_id)
        Alerter.set_asset_id(asset_id)

        case_results = {
            "flow_activated": {
                "hole": (
                    (HoleType.CASED_HOLE, 8.835, 0.0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 8.5, 9891.0, 14901.07),
                    (HoleType.OPEN_HOLE, 12.0, 14901.07, 20539.77),
                    (HoleType.OPEN_HOLE, 8.5, 20539.77, 20633.0)
                ),
                "annulus": (
                    (HoleType.CASED_HOLE, 8.835, 5.0, 0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 5.0, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 8.5, 5.0, 9891.0, 14901.07),
                    (HoleType.OPEN_HOLE, 12.0, 5.0, 14901.07, 20528.9),
                    (HoleType.OPEN_HOLE, 12.0, 8.25, 20528.9, 20539.77),
                    (HoleType.OPEN_HOLE, 8.5, 6.75, 20539.77, 20633.0),
                )
            },
            "open_hole_activated": {
                "hole": (
                    (HoleType.CASED_HOLE, 8.835, 0.0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 12.0, 9891.0, 20539.77),
                    (HoleType.OPEN_HOLE, 8.5, 20539.77, 20633.0)
                ),
                "annulus": (
                    (HoleType.CASED_HOLE, 8.835, 5.0, 0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 5.0, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 12.0, 5.0, 9891.0, 20528.9),
                    (HoleType.OPEN_HOLE, 12.0, 8.25, 20528.9, 20539.77),
                    (HoleType.OPEN_HOLE, 8.5, 6.75, 20539.77, 20633.0),
                )
            },
            "unactivated": {
                "hole": (
                    (HoleType.CASED_HOLE, 8.835, 0.0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 8.5, 9891.0, 20633.0)
                ),
                "annulus": (
                    (HoleType.CASED_HOLE, 8.835, 5.0, 0, 9890.0),
                    (HoleType.OPEN_HOLE, 8.75, 5.0, 9890.0, 9891.0),
                    (HoleType.OPEN_HOLE, 8.5, 5.0, 9891.0, 20528.9),
                    (HoleType.OPEN_HOLE, 8.5, 8.25, 20528.9, 20539.77),
                    (HoleType.OPEN_HOLE, 8.5, 6.75, 20539.77, 20633.0),
                )
            }
        }

        def get_under_reamer_from_api(mongo_id):
            drillstring = get_config_by_id(mongo_id, collection="data.drillstring")
            components = drillstring.get("data", {}).get("components", [])
            return next((component for component in components if component.get("family") == "ur"), {})

        for activation_type, expected_values in case_results.items():
            print(f"\nCase: Under-reamer is {activation_type}")
            # Set the environment variable to simulate that this is a task app
            os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "unit-testing-lambda-task"

            wits_json_file = os.path.abspath(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits_under_reamer.json")
            )

            # Reset Drillstring
            reset_drillstring(activation_type)

            wits = file_to_json(wits_json_file)
            self.run_under_reamer_case(wits, expected_values)

            # Assert drillstring on API is not updated becuase it is not triggered from a stream app
            # The method above `reset_drillstring` resets the drillstring to original condition
            # The original condition for this test case are:
            #    UR_ACTIVE :   `ur_opened_depth` is set to `None`
            #    UR_INACTIVE:  `ur_opened_depth` is set to `10_000_000`
            # When running from this test case, the api should not be updated, and above values should be present on api
            # Following assertions ensure that. However when running from stream app, the api will be updated

            _id = wits["metadata"]["drillstring"]
            under_reamer_component = get_under_reamer_from_api(_id)

            if activation_type == "unactivated":
                self.assertEqual(10_000_000.0, under_reamer_component.get("ur_opened_depth"))
            else:
                self.assertIsNone(under_reamer_component.get("ur_opened_depth"))

        print("\nCase: Running UR test to ensure that API is actually updated when running from a stream app")
        # Set the environment variable to simulate that this is not a task app
        os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "unit-testing-lambda"
        expected_values = case_results.get("flow_activated")
        wits_json_file = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits_under_reamer.json")
        )
        reset_drillstring("flow_activated")
        wits = file_to_json(wits_json_file)
        self.run_under_reamer_case(wits, expected_values)
        _id = wits["metadata"]["drillstring"]
        under_reamer_component = get_under_reamer_from_api(_id)
        # Assert that api was actually updated in this test case becuase it simulates a stream app
        self.assertEqual(14901.07, under_reamer_component.get("ur_opened_depth"))

    def test_overlapping_liners(self):
        """
        In this test case we are checking if the casings and liners
        are set correctly even if the there are overlapping liners.
        :return:
        """

        wits = get_one_data_record(asset_id=3083, collection="wits")
        wellbore = run_drillstring_and_create_wellbore(wits)

        hole: Hole = wellbore.actual_hole
        hole_depth = 25633.01

        self.assertEqual(10, len(hole))

        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertAlmostEqual(0.0, hole[0].top_depth, 1)
        self.assertAlmostEqual(11863.3, hole[0].bottom_depth, 1)
        self.assertAlmostEqual(4.67, hole[0].inner_diameter, delta=0.01)

        self.assertEqual(HoleType.CASED_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(11863.3, hole[1].top_depth, 1)
        self.assertAlmostEqual(11902.0, hole[1].bottom_depth, 1)
        self.assertAlmostEqual(4.28, hole[1].inner_diameter, delta=0.01)

        self.assertEqual(HoleType.CASED_HOLE, hole[8].hole_type)
        self.assertAlmostEqual(20610.0, hole[8].top_depth, 1)
        self.assertAlmostEqual(23000.0, hole[8].bottom_depth, 1)
        self.assertAlmostEqual(3.0, hole[8].inner_diameter, delta=0.01)

        self.assertEqual(HoleType.OPEN_HOLE, hole[9].hole_type)
        self.assertAlmostEqual(23000.0, hole[9].top_depth, 1)
        self.assertAlmostEqual(hole_depth, hole[9].bottom_depth, 1)
        self.assertAlmostEqual(2.85, hole[9].inner_diameter, delta=0.01)

    def test_creating_wellbore_with_missing_drillstring(self):
        wits_record = {
            "collection": "wits",
            "asset_id": 10477107,
            "metadata": {
                'drillstring': '5f4d5bf1150c40007f3a12fc'
            },
            "data": {
                "bit_depth": 1111,
                "hole_depth": 1111
            }
        }

        wellbore = run_drillstring_and_create_wellbore(wits_record)
        self.assertIsNone(wellbore)

    def test_multiple_casings(self):
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        # DS 5 of Odysseus well
        asset_id = 88739932
        Logger.set_asset_id(asset_id)

        wits = {
            "asset_id": asset_id,
            "metadata": {
                "drillstring": "5fda35ce1c5c89001ce626d2",
            },
            "data": {
                "bit_depth": 15_000.0,
                "hole_depth": 15_000.0
            }
        }

        expected_results = {
            "hole": (
                (HoleType.CASED_HOLE, 12.0, 0.0, 1500.0),  # Riser
                (HoleType.CASED_HOLE, 28.0, 1500.0, 1700.0),  # Conductor
                (HoleType.CASED_HOLE, 8.835, 1700.0, 9907.0),  # Intermediate casing
                (HoleType.OPEN_HOLE, 8.75, 9907.0, 15000.0),
            ),
            "annulus": (
                (HoleType.CASED_HOLE, 12, 5, 0.0, 1500.0),
                (HoleType.CASED_HOLE, 28, 5, 1500.0, 1700.0),
                (HoleType.CASED_HOLE, 8.835, 5, 1700.0, 9907.0),
                (HoleType.OPEN_HOLE, 8.75, 5, 9907.0, 14897.68),
                (HoleType.OPEN_HOLE, 8.75, 6.69, 14897.68, 14959.63),
                (HoleType.OPEN_HOLE, 8.75, 6.75, 14959.63, 14961.95),
                (HoleType.OPEN_HOLE, 8.75, 6.81, 14961.95, 14971.61),
                (HoleType.OPEN_HOLE, 8.75, 6.75, 14971.61, 15000.0)
            )
        }

        wellbore = run_drillstring_and_create_wellbore(wits)
        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)
        self.assert_hole(expected_results.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_results.get("annulus"), annulus)

    def test_consecutive_casings(self):
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        # Riser of Odysseus well
        asset_id = 88739932
        Logger.set_asset_id(asset_id)

        wits = {
            "asset_id": asset_id,
            "metadata": {
                "casing": "5fda3772a7e939001c289bd8"
            },
            "data": {
                "bit_depth": 1_000.0,
                "hole_depth": 2_338.0
            }
        }

        expected_results = {
            "hole": (
                (HoleType.CASED_HOLE, 28.0, 1500.0, 1700.0),  # Conductor casing
                (HoleType.CASED_HOLE, 12.415, 1700.0, 2338.0)  # Surface Casing
            ),
            "annulus": ()
        }

        wellbore = run_casingstring_and_create_wellbore(wits)
        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)
        self.assert_hole(expected_results.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_results.get("annulus"), annulus)

    def test_detailed_liner(self):
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        asset_id = 13684306
        Logger.set_asset_id(asset_id)

        wits = {
            "asset_id": asset_id,
            "metadata": {
                "drillstring": "5fbe0ec8eb6ace1f53efdd01"
            },
            "data": {
                "bit_depth": 9700.0,
                "hole_depth": 9700.0
            }
        }

        expected_results = {
            "hole": (
                (HoleType.CASED_HOLE, 8.84, 0.0, 5494.0),
                (HoleType.CASED_HOLE, 6.88, 5494.0, 8483.0),
                (HoleType.CASED_HOLE, 6.88, 8483.0, 8525.0),
                (HoleType.CASED_HOLE, 6.8, 8525.0, 8567.0),
                (HoleType.OPEN_HOLE, 6.75, 8567.0, 9700.0)
            ),
            "annulus": (
                (HoleType.CASED_HOLE, 8.84, 4.50, 0, 5494.0),
                (HoleType.CASED_HOLE, 6.88, 4.50, 5494.0, 8525.0),
                (HoleType.CASED_HOLE, 6.8, 4.50, 8525.0, 8567.0),
                (HoleType.OPEN_HOLE, 6.75, 4.50, 8567.0, 9581.61),
                (HoleType.OPEN_HOLE, 6.75, 5.25, 9581.61, 9586.27),
                (HoleType.OPEN_HOLE, 6.75, 5.12, 9586.27, 9618.66),
                (HoleType.OPEN_HOLE, 6.75, 4.88, 9618.66, 9635.90),
                (HoleType.OPEN_HOLE, 6.75, 5.06, 9635.90, 9642.27),
                (HoleType.OPEN_HOLE, 6.75, 4.81, 9642.27, 9647.48),
                (HoleType.OPEN_HOLE, 6.75, 4.75, 9647.48, 9651.15),
                (HoleType.OPEN_HOLE, 6.75, 5.19, 9651.15, 9680.84),
                (HoleType.OPEN_HOLE, 6.75, 5.25, 9680.84, 9685.21),
                (HoleType.OPEN_HOLE, 6.75, 4.81, 9685.21, 9700.0),
            )
        }

        wellbore = run_drillstring_and_create_wellbore(wits)
        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)
        self.assert_hole(expected_results.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_results.get("annulus"), annulus)

    def test_detailed_liner_while_running(self):
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        asset_id = 13684306
        Logger.set_asset_id(asset_id)

        wits = {
            "asset_id": asset_id,
            "metadata": {
                "casing": "5fbe0ec8eb6ace1f53efdcfe"
            },
            "data": {
                "bit_depth": 8_000.0,
                "hole_depth": 8_568.0
            }
        }

        expected_results = {
            "hole": (
                (HoleType.CASED_HOLE, 8.84, 0.0, 5710.0),
                (HoleType.OPEN_HOLE, 8.75, 5710.0, 8568.0)
            ),
            "annulus": (
                (HoleType.CASED_HOLE, 8.84, 5.0, 0, 5017.41),
                (HoleType.CASED_HOLE, 8.84, 7.63, 5017.41, 5710.0),
                (HoleType.OPEN_HOLE, 8.75, 7.63, 5710.0, 7956.0),
                (HoleType.OPEN_HOLE, 8.75, 7.5, 7956.0, 8000.0)
            )
        }

        wellbore = run_casingstring_and_create_wellbore(wits)
        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)
        self.assert_hole(expected_results.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_results.get("annulus"), annulus)

    def test_riser_boostline(self):
        os.environ["LOGGING_LEVEL"] = "debug"
        os.environ["LOGGING_ASSET_ID"] = "all"

        asset_id = 35629349
        Logger.set_asset_id(asset_id)

        wits = {
            "asset_id": asset_id,
            "metadata": {
                "drillstring": "5f8f46edb2ce18420cc43eb4"
            },
            "data": {
                "bit_depth": 21_000.0,
                "hole_depth": 21_000.0
            }
        }

        expected_results = {
            "hole": (
                (HoleType.CASED_HOLE, 7.0, 0.0, 10142.0),
                (HoleType.CASED_HOLE, 6.5, 10142.0, 20551.0),
                (HoleType.CASED_HOLE, 6.5, 20551.0, 20591.0),
                (HoleType.OPEN_HOLE, 6.0, 20591.0, 21000.0)
            ),
            "annulus": (
                (HoleType.CASED_HOLE, 7.0, 4.0, 0, 10142.0),
                (HoleType.CASED_HOLE, 6.5, 4.0, 10142.0, 17858.88),
                (HoleType.CASED_HOLE, 6.5, 4.75, 17858.88, 17870.02),
                (HoleType.CASED_HOLE, 6.5, 5.0, 17870.02, 17881.59),
                (HoleType.CASED_HOLE, 6.5, 4.0, 17881.59, 20591.0),
                (HoleType.OPEN_HOLE, 6.0, 4.0, 20591.0, 20778.74),
                (HoleType.OPEN_HOLE, 6.0, 4.9, 20778.74, 20783.23),
                (HoleType.OPEN_HOLE, 6.0, 4.0, 20783.23, 20846.14),
                (HoleType.OPEN_HOLE, 6.0, 4.81, 20846.14, 20849.25),
                (HoleType.OPEN_HOLE, 6.0, 4.75, 20849.25, 20852.34),
                (HoleType.OPEN_HOLE, 6.0, 5.0, 20852.34, 20883.62),
                (HoleType.OPEN_HOLE, 6.0, 4.75, 20883.62, 20913.60),
                (HoleType.OPEN_HOLE, 6.0, 4.56, 20913.60, 20941.39),
                (HoleType.OPEN_HOLE, 6.0, 4.62, 20941.39, 20969.18),
                (HoleType.OPEN_HOLE, 6.0, 5.0, 20969.18, 21000.0),
            )
        }

        wellbore = run_drillstring_and_create_wellbore(wits)
        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)
        self.assert_hole(expected_results.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_results.get("annulus"), annulus)

    def test_riserless(self):
        wits_json_file = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits_riserless.json")
        )
        wits = file_to_json(wits_json_file)
        wellbore = run_drillstring_and_create_wellbore(wits)

        hole: Hole = wellbore.actual_hole

        self.assertEqual(3, len(hole))

        self.assertEqual(HoleType.CASED_HOLE, hole[0].hole_type)
        self.assertAlmostEqual(3000.0, hole[0].top_depth, 1)
        self.assertAlmostEqual(10000.0, hole[0].bottom_depth, 1)
        self.assertAlmostEqual(7000.0, hole[0].length, 1)
        self.assertAlmostEqual(12.415, hole[0].inner_diameter, delta=0.01)

        # Under reamer open hole
        self.assertEqual(HoleType.OPEN_HOLE, hole[1].hole_type)
        self.assertAlmostEqual(10_000.0, hole[1].top_depth, 1)
        self.assertAlmostEqual(14_906.77, hole[1].bottom_depth, delta=0.1)
        self.assertAlmostEqual(4_906.77, hole[1].length, delta=0.1)
        self.assertAlmostEqual(12.0, hole[1].inner_diameter, delta=0.01)

        # Bit sized open hole
        self.assertEqual(HoleType.OPEN_HOLE, hole[2].hole_type)
        self.assertAlmostEqual(14_906.77, hole[2].top_depth, delta=0.1)
        self.assertAlmostEqual(15000, hole[2].bottom_depth, 1)
        self.assertAlmostEqual(93.23, hole[2].length, delta=0.1)
        self.assertAlmostEqual(8.5, hole[2].inner_diameter, delta=0.01)

        drillstring = wellbore.actual_drillstring
        self.assertAlmostEqual(0.0, drillstring[0].top_depth, 1)
        self.assertAlmostEqual(15_000.0, drillstring[-1].bottom_depth, 1)

        annulus = wellbore.actual_annulus
        self.assertEqual(HoleType.CASED_HOLE, annulus[0].hole_type)
        self.assertAlmostEqual(3_000.0, annulus[0].top_depth, 1)
        self.assertAlmostEqual(10_000.0, annulus[0].bottom_depth, 1)
        self.assertAlmostEqual(12.415, annulus[0].inner_diameter_hole, delta=0.01)

        self.assertEqual(HoleType.OPEN_HOLE, annulus[1].hole_type)
        self.assertAlmostEqual(10_000.0, annulus[1].top_depth, 1)
        self.assertAlmostEqual(14_895.9, annulus[1].bottom_depth, 1)
        self.assertAlmostEqual(12.0, annulus[1].inner_diameter_hole, delta=0.01)

        self.assertEqual(HoleType.OPEN_HOLE, annulus[3].hole_type)
        self.assertAlmostEqual(14906.77, annulus[3].top_depth, 1)
        self.assertAlmostEqual(15_000.0, annulus[3].bottom_depth, 1)
        self.assertAlmostEqual(8.5, annulus[3].inner_diameter_hole, delta=0.01)

    def assert_annulus(self, expected_annulus: tuple, actual_annulus: Annulus):
        expected_number_of_sections = len(expected_annulus)
        self.assertEqual(expected_number_of_sections, len(actual_annulus))

        for i in range(expected_number_of_sections):
            actual_annulus_section = (
                actual_annulus[i].hole_type,
                actual_annulus[i].inner_diameter_hole,
                round(actual_annulus[i].outer_diameter_pipe, 2),
                round(actual_annulus[i].top_depth, 2),
                round(actual_annulus[i].bottom_depth, 2)
            )
            expected_annulus_section = expected_annulus[i]
            self.assertEqual(expected_annulus_section, actual_annulus_section)

    def assert_hole(self, expected_hole: tuple, actual_hole: Hole):
        expected_number_of_sections = len(expected_hole)
        self.assertEqual(expected_number_of_sections, len(actual_hole))

        for i in range(expected_number_of_sections):
            actual_hole_section = (
                actual_hole[i].hole_type,
                actual_hole[i].inner_diameter,
                round(actual_hole[i].top_depth, 2),
                round(actual_hole[i].bottom_depth, 2)
            )
            expected_hole_section = expected_hole[i]
            self.assertEqual(expected_hole_section, actual_hole_section)

    def run_under_reamer_case(self, wits, expected_values):
        wellbore = run_drillstring_and_create_wellbore(wits)

        # Activate under-reamer in cased hole
        # This should raise an alert in console with WARN
        bit_depth = 9000.17
        hole_depth = 15005.17
        mud_flow_rate = 521.25
        wellbore.update(bit_depth, hole_depth, mud_flow_rate)

        # Update to activation depth and increase mud flow rate
        bit_depth = 15005.17
        hole_depth = 15005.17
        mud_flow_rate = 521.25
        wellbore.update(bit_depth, hole_depth, mud_flow_rate)

        # Update to target depth
        bit_depth = 20633.00
        hole_depth = 20633.00
        mud_flow_rate = 521.25
        wellbore.update(bit_depth, hole_depth, mud_flow_rate)

        # test serialization
        ser_str = obj2json(wellbore)
        wellbore_des = json2obj(ser_str)
        self.assertEqual(len(wellbore.actual_drillstring), len(wellbore_des.actual_drillstring))
        self.assertAlmostEqual(wellbore.actual_drillstring[1].inner_diameter, wellbore_des.actual_drillstring[1].inner_diameter, 10)
        self.assertAlmostEqual(wellbore.actual_drillstring[1].top_depth, wellbore_des.actual_drillstring[1].top_depth, 10)

        hole = wellbore.actual_hole
        annulus = wellbore.actual_annulus

        # Assert hole configuration
        print("\n Hole configuration is:")
        print(hole)

        self.assert_hole(expected_values.get("hole"), hole)

        # Assert annulus configuration
        print("\n Annulus configuration is:")
        print(annulus)
        self.assert_annulus(expected_values.get("annulus"), annulus)


def get_wits():
    wits_json_file = os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "test", "wits.json")
    )
    return file_to_json(wits_json_file)


def reset_drillstring(activation_type="flow_activated"):
    activation_depth = None
    if activation_type == "unactivated":
        activation_type = "flow_activated"
        activation_depth = 10_000_000.0

    api_worker = API()
    path = "/v1/data/corva/data.drillstring/5ebaceeac93924003a922593"
    drillstring = api_worker.get(path=path).data
    drillstring["data"]["start_depth"] = 9891
    for component in drillstring["data"]["components"]:
        if component.get("family") == "ur":
            component["ur_opened_depth"] = activation_depth
            component["activation_logic"] = activation_type
            break

    api_worker.post(path="/v1/data/corva/data.drillstring", data=json.dumps(drillstring))
