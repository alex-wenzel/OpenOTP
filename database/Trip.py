from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Trip(Base):
	__tablename__ = "trip"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		primary_key = True, 
		nullable = False
	)
	route_id: Mapped[str] = mapped_column(
		String(3), 
		nullable = False
	)
	trip_id: Mapped[int] = mapped_column(
		primary_key = True, 
		nullable = False
	)
	trip_headsign: Mapped[str] = mapped_column(
		String(32), 
		nullable = False
	)
	block_id: Mapped[str] = mapped_column(
		String(6), 
		nullable = False
	)
	trip_headsign_short: Mapped[str] = mapped_column(
		String(32), 
		nullable = False
	)
	shakeup = relationship(
		"Shakeup", 
		foreign_keys = "Shakeup.shakeup_id"
	)
	route = relationship(
		"Route",
		foreign_keys = "Route.route_id"
	)