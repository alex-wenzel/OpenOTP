from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Shakeup(Base): 
	__tablename__ = "shakeup"

	shakeup_id: Mapped[str] = mapped_column(
		String(7), 
		primary_key = True, 
		nullable = False
	)
	start: Mapped[datetime] = mapped_column(
		DateTime, 
		nullable = False
	)
	end: Mapped[datetime] = mapped_column(
		DateTime, 
		nullable = False
	)