import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Boolean, Float, Integer, SmallInteger
from typing import cast, List, TYPE_CHECKING

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import StopTimeRow

if TYPE_CHECKING:
	from app.models.Trip import Trip


class StopTime(db.Model, StaticGTFSTable):
	__tablename__ = "static_stop_times"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	## 4 bytes
	trip_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("static_trips.trip_id"),
		primary_key = True
	)
	## 4 bytes
	departure_time: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	## 4 bytes
	stop_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("static_stops.stop_id")
	)
	## 4 bytes
	shape_dist_traveled: Mapped[float] = db.orm.mapped_column(
		Float(3),
		nullable = False
	)
	## 2 bytes
	stop_sequence: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		nullable = False,
		primary_key = True
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("shakeups.shakeup_id")
	)
	## 1 byte
	timepoint: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)

	## Relationships

	trip: Mapped["Trip"] = db.orm.relationship(
		back_populates = "stop_times"
	)

	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["StopTime"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["StopTime"] = []

		for _, row in table_df.iterrows():

			row_d = cast("StopTimeRow", row.to_dict())

			objs.append(cls(
				trip_id = row_d["trip_id"],
				departure_time = cls.clocktime_to_int(
					row_d["departure_time"]
				),
				stop_id = row_d["stop_id"],
				shape_dist_traveled = row_d["shape_dist_traveled"],
				stop_sequence = row_d["stop_sequence"],
				shakeup_id = shakeup_id,
				timepoint = bool(row_d["timepoint"])
			))

		return objs