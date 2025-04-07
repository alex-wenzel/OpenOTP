from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Integer, SmallInteger, String, Text
from typing import cast, List
import pandas as pd

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import ServiceExceptionRow
from app.models.Shakeup import Shakeup


class ServiceException(db.Model, StaticGTFSTable):
	__tablename__ = "static_service_exceptions"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	## Variable bytes
	service_id: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False,
		primary_key = True
	)
	## 4 bytes
	date: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False,
		primary_key = True
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		#SmallInteger,
		#nullable = False
		ForeignKey("shakeups.shakeup_id")
	)
	## 1 byte
	exception_type: Mapped[str] = db.orm.mapped_column(
		String(1),
		nullable = False
	)

	## Relationships

	shakeup: Mapped[Shakeup] = db.orm.relationship(
		back_populates = "service_exceptions"
	)

	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["ServiceException"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["ServiceException"] = []

		for _, row in table_df.iterrows():
			row_d = cast("ServiceExceptionRow", row.to_dict())

			objs.append(cls(
				service_id = row_d["service_id"],
				date = row_d["date"],
				exception_type = str(row_d["exception_type"]),
				shakeup_id = shakeup_id
			))

		return objs