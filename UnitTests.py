import datetime
import pytz
import unittest

from Data import LiveRecord
from Utils import ts2dt


class Test_Data_LiveRecord(unittest.TestCase):
	def test_input_check(self):
		with self.assertRaisesRegex(ValueError, "Must initialize LiveRecord"):
			LiveRecord(
				row = 1, ## Wrong type, but should still trigger error
				trip_id = "1",
				vehicle_id = "1",
				next_stop_id = "1",
				next_stop_departure = datetime.datetime.now(),
				live_feed_timestamp = datetime.datetime.now()
			)


class Test_Utils_ts2dt(unittest.TestCase):
	def test_str2dt(self):
		dt1 = ts2dt(1715105414)
		self.assertEqual(dt1.month, 5)
		self.assertEqual(dt1.tzinfo.zone, "America/Los_Angeles")
		self.assertEqual(dt1.hour, 11)

		dt2 = ts2dt(1715105414 + 7200)
		self.assertEqual(dt2.hour, 13)