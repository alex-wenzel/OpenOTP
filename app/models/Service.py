import pandas as pd
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy.types import Boolean, Integer, Text
from typing import cast, Dict, List, Mapping

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import ServiceRow
from app.models.Shakeup import Shakeup
from app.models.Trip import Trip


class Service(db.Model, StaticGTFSTable):
	__tablename__ = "static_services"

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
		ForeignKey("shakeups.shakeup_id"),
	)
	## 1 byte
	monday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	tuesday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	wednesday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	thursday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	friday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	saturday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)
	## 1 byte
	sunday: Mapped[bool] = db.orm.mapped_column(
		Boolean,
		nullable = False
	)

	## Relationships

	trips: Mapped[List["Trip"]] = db.orm.relationship(
		back_populates = "service"
	)

	shakeup: Mapped["Shakeup"] = db.orm.relationship(
		back_populates = "services"
	)


	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["Service"]:
		table_df = pd.read_csv(table_path)

		objs: List["Service"] = []

		for _, row in table_df.iterrows():
			row_d = cast("ServiceRow", row.to_dict())

			objs.append(cls(
				service_id = row_d["service_id"],
				start_date = row_d["start_date"],
				end_date = row_d["end_date"],
				monday = bool(row_d["monday"]),
				tuesday = bool(row_d["tuesday"]),
				wednesday = bool(row_d["wednesday"]),
				thursday = bool(row_d["thursday"]),
				friday = bool(row_d["friday"]),
				saturday = bool(row_d["saturday"]),
				sunday = bool(row_d["sunday"]),
				shakeup_id = shakeup_id
			))

		return objs


