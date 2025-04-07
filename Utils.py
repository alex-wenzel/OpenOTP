from datetime import date
import sys
from sqlalchemy.exc import SQLAlchemyError
from typing import Any, Callable, List, Optional, TypeVar 

def hprint(msg: Any) -> None:
	"""
	Printing with stdout flush for Heroku logging.
	"""
	print(msg)
	sys.stdout.flush()

T = TypeVar("T")

def none_if_sa_error(func: Callable[..., T]) -> Callable[..., Optional[T]]:
	def inner(*args, **kwargs) -> Optional[T]:
		try:
			return func(*args, **kwargs)
		except SQLAlchemyError:
			return None
		
	return inner

def empty_list_if_sa_error(func: Callable[...,List[T]]) -> Callable[..., List[T]]:
	def inner(*args, **kwargs) -> List[T]:
		try:
			return func(*args, **kwargs)
		except SQLAlchemyError:
			return []
	
	return inner

def date_to_int(
	query_date: date
) -> int:
	return int(query_date.strftime("%Y%m%d"))