from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Stop(Base):
	__tablename__ = "stop"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		primary_key = True, 
		nullable = False
	)
	stop_id: Mapped[str] = mapped_column(
		String(5), 
		primary_key = True, 
		nullable = False
	)
	stop_name: Mapped[str] = mapped_column(
		String(256), 
		nullable = False
	)
	stop_name_short: Mapped[str] = mapped_column(
		String(32), 
		nullable = False
	)
	shakeup = relationship(
		"Shakeup", 
		foreign_keys = "Shakeup.shakeup_id"
	)