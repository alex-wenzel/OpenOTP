from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Route(Base):
	__tablename__ = "route"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		primary_key = True, 
		nullable = False
	)
	route_id: Mapped[str] = mapped_column(
		String(3), 
		primary_key = True, 
		nullable = False
	) 
	route_short_name: Mapped[str] = mapped_column(
		String(6), 
		nullable = False
	)
	route_long_name: Mapped[str] = mapped_column(
		String(256), 
		nullable = False
	)
	route_group: Mapped[str] = mapped_column(
		String(11), 
		nullable = False
	)
	shakeup = relationship(
		"Shakeup", 
		foreign_keys = "Shakeup.shakeup_id"
	)