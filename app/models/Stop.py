import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Integer, Text
from typing import cast, List

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import StopRow

from utils import hprint


class Stop(db.Model, StaticGTFSTable):
	__tablename__ = "static_stops"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	## Variable bytes
	stop_name: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## Variable bytes
	stop_name_short: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## 4 bytes
	stop_id: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False,
		primary_key = True
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("shakeups.shakeup_id")
	)

	## Relationships

	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["Stop"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["Stop"] = []

		for _, row in table_df.iterrows():

			row_d = cast("StopRow", row.to_dict())

			try:
				int(row_d["stop_id"])
			except ValueError:
				## Skipping non-int stop IDs because they aren't needed. 
				stop_id = row_d["stop_id"]
				hprint(f"Skipping stop '{stop_id}'")
				continue

			objs.append(cls(
				stop_name = row_d["stop_name"],
				stop_name_short = row_d["stop_name_short"],
				stop_id = int(row_d["stop_id"]),
				shakeup_id = shakeup_id
			))

		return objs