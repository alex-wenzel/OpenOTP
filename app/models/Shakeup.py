from sqlalchemy.orm import Mapped, backref
from sqlalchemy.types import Integer, SmallInteger, String
from typing import List, TYPE_CHECKING

from app.extensions import db

if TYPE_CHECKING:
	from app.models.Service import Service
	from app.models.ServiceException import ServiceException

#from app.models.Service import Service
#from app.models.ServiceException import ServiceException


## Additional table for allowing multiple service changes
## worth of data to exist in the same database
class Shakeup(db.Model):
	__tablename__ = "shakeups"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)
	
	## Data

	## 7 bytes
	shakeup_name: Mapped[str] = db.orm.mapped_column(
		String(7),
		nullable = False,
		unique = True
	)
	## 4 bytes
	start_date: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	## 4 bytes
	end_date: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		primary_key = True,
		nullable = False
	)

	##Relationships

	services: Mapped[List["Service"]] = db.orm.relationship(
		back_populates = "shakeup"
	)

	service_exceptions: Mapped[List["ServiceException"]] = db.orm.relationship(
		back_populates = "shakeup"
	)

	## Functions