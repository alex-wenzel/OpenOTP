"""
Generally applicable data wrangling + conversion functions.
"""


from datetime import datetime
import pytz
from typing import Any, Union


def ts2dt(
	ts: Union[float, int]
) -> datetime:
	
	"""
	Converts a unix timestamp to a datetime object. Timestamps are assumed
	to be standard Unix timestamps (i.e., GMT). This codebase is currently
	hardcoded to operate explicitly in California (pytz "America/Los_Angeles").

	Parameters
	----------
	ts : float, int
		The timestamp input.

	Returns
	-------
	datetime
		The datetime object representing `ts`, is timezone-aware 
		for "America/Los_Angeles"
	"""
	return datetime.fromtimestamp(
		ts, 
		tz = pytz.timezone("America/Los_Angeles")
	)


def enforce_not_None(
	x: Any
) -> Any:
	
	"""
	Returns the value provided if it isn't None, otherwise raises a ValueError. 
	Purpose of this function is to reduce long if/else blocks in data representation
	class initializations. 

	Parameters
	----------
	x : any
		The object to check 

	Returns
	-------
	type(x)
		The same object x, as long as it isn't None
	"""
	if x is None:
		raise ValueError(f"Object {x} cannot be None in this context.")
	return x







