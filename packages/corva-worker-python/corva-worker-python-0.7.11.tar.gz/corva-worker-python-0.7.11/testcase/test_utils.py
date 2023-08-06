import os
import unittest
import numpy as np
from worker.data import math
from worker.data import operations
from worker.data.operations import compare_float, is_stream_app


class TestGeneral(unittest.TestCase):
    def test_operations(self):
        self.assertFalse(operations.is_number("nan"))
        self.assertFalse(operations.is_number(None))
        self.assertFalse(operations.is_number(""))
        self.assertFalse(operations.is_number(''))
        self.assertFalse(operations.is_number("null"))
        self.assertFalse(operations.is_number(np.nanpercentile([np.nan], 50)))
        self.assertTrue(operations.is_number(-999.25))
        self.assertTrue(operations.is_number("-999.25"))
        self.assertTrue(operations.is_number("0.0"))

        self.assertTrue(operations.is_number(float('inf')))
        self.assertFalse(operations.is_finite(float('inf')))

        self.assertTrue(operations.is_finite(1.1))
        self.assertFalse(operations.is_finite("1.1"))

        self.assertIsNone(operations.to_number("nan"))
        self.assertIsNone(operations.to_number(""))
        self.assertIsNone(operations.to_number(''))
        self.assertIsNone(operations.to_number("null"))
        self.assertEqual(operations.to_number(-999.25), -999.25)
        self.assertEqual(operations.to_number("-999.25"), -999.25)
        self.assertEqual(operations.to_number("0.0"), 0.0)

        np.testing.assert_equal(operations.none_to_nan(None), np.nan)
        np.testing.assert_equal(operations.none_to_nan(np.nan), np.nan)
        np.testing.assert_equal(operations.none_to_nan(1), 1)
        np.testing.assert_equal(operations.none_to_nan([1, 2, None]), [1, 2, np.nan])
        np.testing.assert_equal(operations.none_to_nan([1, 2, 3, np.nan, None]), [1, 2, 3, np.nan, np.nan])

        # Test is_task_app
        os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "test.operation-task"
        self.assertFalse(is_stream_app())
        os.environ["AWS_LAMBDA_FUNCTION_NAME"] = "test.operation"
        self.assertTrue(is_stream_app())

        self.assertEqual(0, compare_float(1.1, 1.1, 0))
        self.assertEqual(0, compare_float(1.0, 1.1, 0.1))
        self.assertEqual(-1, compare_float(1.0, 1.1, 0))
        self.assertEqual(-1, compare_float(1.0, 1.1, 0.05))
        self.assertEqual(1, compare_float(1.1, 1, 0))
        self.assertEqual(1, compare_float(1.1, 1, 0.05))
        self.assertEqual(-1, compare_float(-1.1, -1, 0.05))

    def test_fetch_from_path(self):
        self.assertTrue(operations.get_data_by_path(dict(name="X", value=2.3), 'value', float), 2.3)
        self.assertTrue(operations.get_data_by_path(dict(name="X", value=2.3), 'property', float, default=1.0), 1.0)

        self.assertTrue(operations.get_data_by_path(dict(name={'first_name': 'foo', 'last_name': 'bar'}, value=2.3), 'name.first_name'), 'foo')
        self.assertTrue(operations.get_data_by_path(dict(p1={'p2': 1.2}), 'p1.p2'), 1.2)

        # if default is not provided and the key can not be found it will raise an exception
        self.assertRaises(Exception, operations.get_data_by_path, {"key": "value"}, "a_path")
        # if default is provided (even None) and the key can not be found it return the default value
        self.assertIsNone(operations.get_data_by_path({"key": "value"}, "a_path", default=None))
        self.assertEqual("something", operations.get_data_by_path(data={"key": "value"}, path="a_path", default="something"))

    def test_math_utils(self):
        self.assertEqual(math.percentile([1, 2, None, np.nan], 50), 1.5)
        self.assertEqual(math.percentile([None, 1, np.nan], 50), 1.0)
        self.assertIsNone(math.percentile([np.nan, np.nan], 50))
        self.assertIsNone(math.percentile([None], 50))

        mean_angle = math.mean_angles([248, 315, 174, 112, 236, 276, 276, 39, 270, 231, 259, 186, 298])
        self.assertTrue(253 < mean_angle < 254)
        self.assertTrue(2.999 <= math.mean_angles([1, 2, 3, 4, 5]) <= 3.001)
        self.assertTrue(356.999 <= math.mean_angles([-1, -2, -3, -4, -5]) <= 357.001)

        self.assertEqual(math.angle_difference(10, 350), -20.0)
        self.assertEqual(math.angle_difference(350, 10), 20.0)

        self.assertEqual(math.abs_angle_difference(10, 350), 20.0)
        self.assertEqual(math.abs_angle_difference(350, 10), 20.0)

        self.assertEqual(
            math.split_zip_edges(np.array([0, 1, 2, 4, 6, 8, 9, 10, 12, 14, 15, 16])),
            [(0, 2), (4, 4), (6, 6), (8, 10), (12, 12), (14, 16)]
        )
        self.assertEqual(
            math.split_zip_edges(np.array([0, 1, 2, 4, 6, 8, 9, 10, 12, 14, 15, 16]), min_segment_length=2),
            [(0, 2), (8, 10), (14, 16)]
        )
        self.assertEqual(
            math.split_zip_edges(np.array([0, 1, 2, 4, 8, 9, 10, 12, 14, 15, 16]),
                                 separation_length=2, min_segment_length=2),
            [(0, 4), (8, 16)]
        )

        self.assertEqual(
            math.start_stop([1, 1, 1, 2, 4, 1, 1, 1, 2, 1, 1, 1], 1),
            [(0, 2), (5, 7), (9, 11)]
        )
        self.assertEqual(
            math.start_stop([True, True, True, False, False, True, True, True, False, True, True, True], True),
            [(0, 2), (5, 7), (9, 11)]
        )
