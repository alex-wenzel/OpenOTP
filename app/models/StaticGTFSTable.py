from abc import abstractmethod
from datetime import datetime
from typing import List, TypeVar
from typing_extensions import Self

from app.extensions import db

## Base class for tables
##
## Implements common functionality like converting YYYYMMDD ints 
## to a useful format
KEY_T = TypeVar('KEY_T')

#class StaticGTFSTable(Generic[KEY_T]):
class StaticGTFSTable:
	@staticmethod
	def get_date_from_int(
		date_int: int
	) -> datetime:
		"""
		Parses dates in the form YYYYMMDD

		Parameters
		----------
		date_int : int
			A date in an integer format YYYYMMDD

		Returns
		-------
		datetime
			A datetime object encoding the date shown 
			in date_int (at midnight)
		"""
		return datetime.strptime(
			str(date_int),
			"%Y%m%d"
		)

	@staticmethod
	def get_int_from_date(
		date: datetime
	) -> int:
		"""
		Converts a datetime to the format YYYYMMDD

		Parameters
		----------
		date : datetime
			A datetime object

		Returns
		-------
		int 
			An integer in the format YYYYMMDD
		"""
		return int(date.strftime("%Y%m%d"))


	@staticmethod
	def clocktime_to_int(
		clocktime: str
	) -> int:
		"""
		Converts a timestamp from stop_times to an integer representing
		the number of seconds since midnight. 
		
		Parameters
		----------
		clocktime : str
			A timestamp in (H)H:MM:SS

		Returns
		-------
		int 
			The number of seconds since midnight represented by the timestamp
		"""
		hours, minutes, seconds = list(map(int, clocktime.split(":")))

		return (hours*3600) + (minutes * 60) + seconds
	
	@staticmethod
	def int_to_clocktime(
		timestamp: int
	) -> str:
		"""
		"""
		hours, remainder = divmod(timestamp, 3600)
		minutes, seconds = divmod(remainder, 60)

		return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"

	@classmethod
	@abstractmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List[Self]:
		pass






