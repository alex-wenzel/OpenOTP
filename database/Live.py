from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Live(Base):
	__tablename__ = "live"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		nullable = False
	)
	rec_id: Mapped[int] = mapped_column(
		Integer, 
		primary_key = True, 
		nullable = False
	)
	trip_id: Mapped[int] = mapped_column(
		Integer, 
		nullable = False
	)
	vehicle_id: Mapped[str] = mapped_column(
		String(4), 
		nullable = False
	)
	next_stop_id: Mapped[str] = mapped_column(
		String(5), 
		nullable = False
	)
	next_stop_departure: Mapped[datetime] = mapped_column(
		DateTime, 
		nullable = False
	)
	live_feed_timestamp: Mapped[datetime] = mapped_column(
		DateTime, 
		nullable = False
	)
	shakeup = relationship(
		"Shakeup", 
		foreign_keys = "Shakeup.shakeup_id"
	)
	trip = relationship(
		"Trip",
		foreign_keys = "Trip.trip_id"
	)
	stop = relationship(
		"Stop",
		foreign_keys = "Stop.stop_id"
	)