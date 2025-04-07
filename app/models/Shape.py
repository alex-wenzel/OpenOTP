import pandas as pd
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Float, SmallInteger, Text
from typing import cast, List, TypedDict, TYPE_CHECKING

from app.extensions import db
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import ShapeRow

if TYPE_CHECKING:
	from app.models.Trip import Trip


class Shape(db.Model, StaticGTFSTable):
	"""
	This class does not actually represent the entire shapes.txt file. It
	only contains the length of each shape inside shapes.txt, which is the
	only part of shapes.txt that this application needs. 
	"""
	__tablename__ = "static_shapes"

	## https://stackoverflow.com/questions/33790769/option-to-ignore-extra-keywords-in-an-sqlalchemy-mapped-class-constructor
	def __init__(self, **entries):
		self.__dict__.update(entries)

	## Data

	int_shape_id: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		primary_key = True,
		nullable = False,
		autoincrement = True
	)

	## Variable bytes
	shape_id: Mapped[str] = db.orm.mapped_column(
		Text,
		nullable = False,
		#primary_key = True
	)
	## 4 bytes 
	shape_length: Mapped[float] = db.orm.mapped_column(
		Float(3),
		nullable = False
	)
	## 2 bytes
	shakeup_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("shakeups.shakeup_id")
	)

	## Relationships

	#trips: Mapped[List["Trip"]] = db.orm.relationship(
	#	back_populates = "shape"
	#)
	
	
	## Functions
	@classmethod
	def parse(
		cls,
		table_path: str,
		shakeup_id: int
	) -> List["Shape"]:
		table_df = pd.read_csv(table_path)
		
		objs: List["Shape"] = []

		for _, row in table_df.iterrows():
			row_d = cast("ShapeRow", row.to_dict())

			objs.append(cls(
				shape_id = row_d["shape_id"],
				shape_length = row_d["shape_dist_traveled"],
				shakeup_id = shakeup_id
			))

		return objs