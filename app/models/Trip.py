import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Integer, Text
from typing import cast, List, TYPE_CHECKING

from app.extensions import db
#from app.models.Service import Service
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import TripRow
from app.models.StopTime import StopTime
from app.models.Shape import Shape

if TYPE_CHECKING:
	from app.models.Service import Service
	from app.models.Stop import Stop

from utils import hprint


class Trip(db.Model, StaticGTFSTable):
	__tablename__ = "static_trips"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	## Variable bytes
	route_id: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False,
	)
	## Variable bytes
	service_id: Mapped[str] = db.orm.mapped_column(
		ForeignKey("static_services.service_id")
	)
	## Variable bytes
	trip_headsign: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## Variable bytes
	#int_shape_id: Mapped[int] = db.orm.mapped_column(
	#	ForeignKey("static_shapes.int_shape_id")
	#)
	shape_id: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## 4 bytes
	trip_id: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False,
		primary_key = True
	)
	## 4 bytes
	block_id: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("shakeups.shakeup_id")
	)

	## Relationships

	stop_times: Mapped[List["StopTime"]] = db.orm.relationship(
		back_populates = "trip"
	)

	#shape: Mapped["Shape"] = db.orm.relationship(
	#	back_populates = "trips"
	#)

	service: Mapped["Service"] = db.orm.relationship(
		back_populates = "trips"
	)


	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["Trip"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["Trip"] = []

		for _, row in table_df.iterrows():

			row_d = cast("TripRow", row.to_dict())

			try:
				int(row_d["block_id"])
			except ValueError:
				trip_id = row_d["trip_id"]
				block_id = row_d["block_id"]
				hprint(f"Skipping trip '{trip_id}' in block '{block_id}'")
				continue

			objs.append(cls(
				route_id = row_d["route_id"],
				service_id = row_d["service_id"],
				trip_headsign = row_d["trip_headsign"],
				shape_id = row_d["shape_id"],
				trip_id = row_d["trip_id"],
				block_id = int(row_d["block_id"]),
				shakeup_id = shakeup_id
			))

		return objs