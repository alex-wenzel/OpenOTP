from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class StopTime(Base):
	__tablename__ = "stop_time"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		primary_key = True, 
		nullable = False
	)
	trip_id: Mapped[int] = mapped_column(
		Integer, 
		primary_key = True, 
		nullable = False
	)
	departure_id: Mapped[datetime] = mapped_column(
		DateTime, 
		nullable = False
	)
	stop_id: Mapped[str] = mapped_column(
		String(5), 
		primary_key = True, 
		nullable = False
	)
	stop_sequence: Mapped[int] = mapped_column(
		Integer, 
		nullable = False
	)
	timepoint: Mapped[bool] = mapped_column(
		Boolean, 
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