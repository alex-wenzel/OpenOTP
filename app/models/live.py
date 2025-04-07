from sqlalchemy import ForeignKey
from app.extensions import db
from sqlalchemy.orm import Mapped
from sqlalchemy.types import Integer, SmallInteger
from typing import List


class Query(db.Model):
	__tablename__ = "query"

	query_id: Mapped[int] = db.orm.mapped_column(
		Integer,
		primary_key = True,
		nullable = False
	)
	live_feed_timestamp: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	records: Mapped[List["LiveRecord"]] = db.orm.relationship(
		"LiveRecord",
		back_populates = "query"
	)


class LiveRecord(db.Model):
	__tablename__ = "live_record"

	rec_id: Mapped[int] = db.orm.mapped_column(
		Integer, 
		primary_key = True, 
		nullable = False
	)
	trip_id: Mapped[int] = db.orm.mapped_column(
		Integer, 
		nullable = False
	)
	next_stop_id: Mapped[int] = db.orm.mapped_column(
		Integer,
		nullable = False
	)
	query_id: Mapped[int] = db.orm.mapped_column(
		ForeignKey("query.query_id")
	)
	next_stop_departure: Mapped[int] = db.orm.mapped_column(
		SmallInteger, 
		nullable = True
	)
	vehicle_id: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		nullable = False
	)
	raw_delay: Mapped[int] = db.orm.mapped_column(
		SmallInteger,
		nullable = True
	)
	query: Query = db.orm.relationship(
		Query,
		back_populates = "records"
	)

	def __repr__(self):
		return f'<LiveRecord  {self.rec_id}>'

