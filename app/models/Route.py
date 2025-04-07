import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.types import SmallInteger, String, Text
from typing import cast, Dict, List, Optional

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import RouteRow
from app.models.Trip import Trip


class Route(db.Model, StaticGTFSTable):
	__tablename__ = "static_routes"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	## Variable bytes
	route_long_name: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## Variable bytes
	route_short_name: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False
	)
	## Variable bytes
	route_id: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False,
		primary_key = True
	)
	## Variable bytes
	route_group: Mapped[Optional[str]] = db.orm.mapped_column(
		Text,
		nullable = True,
	)
	## 6 bytes
	route_color: Mapped[str] = db.orm.mapped_column(
		String(6),
		nullable = False
	)
	## 6 bytes
	route_text_color: Mapped[str] = db.orm.mapped_column(
		String(6),
		nullable = False
	)
	## 2 bytes
	route_type: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		nullable = False
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("shakeups.shakeup_id"),
		primary_key = True
	)

	## Relationships

	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["Route"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["Route"] = []

		for _, row in table_df.iterrows():
			row_d = cast("RouteRow", row.to_dict())

			objs.append(cls(
				route_long_name = row_d["route_long_name"],
				route_short_name = row_d["route_short_name"],
				route_id = row_d["route_id"],
				route_group = row_d["route_group"],
				route_color = row_d["route_color"],
				route_text_color = row_d["route_text_color"],
				route_type = row_d["route_type"],
				shakeup_id = shakeup_id
			))

		return objs