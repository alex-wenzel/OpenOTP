from datetime import datetime
from flask import current_app
import os
import pandas as pd
from sqlalchemy.exc import IntegrityError, NoResultFound
import subprocess
from typing import cast, Dict, List, Union

from app.extensions import db
from app.models.Service import Service
from app.models.ServiceException import ServiceException
from app.models.Route import Route
from app.models.Shakeup import Shakeup
from app.models.Shape import Shape
from app.models.StaticGTFSTable import StaticGTFSTable
from app.models.StaticGTFSTableRows import FeedInfoRow
from app.models.Stop import Stop
from app.models.StopTime import StopTime
from app.models.Trip import Trip

from utils import hprint

## Models for which every row from the static txt is brought 1-1 into the database
T_ALL_ROWS_PARSED = Union[
	Service, ServiceException, Route, Stop, StopTime, Trip
]

class StaticGTFS:
	"""
	Not itself a database model, but provides a simpler query 
	interface for things like trips scheduled for a certain date, etc. 
	Also manages checking if current data is present or not. 
	"""
	shakeup: Shakeup


	def __init__(
		self,
		shakeup: Shakeup
	) -> None:
		self.shakeup = shakeup


	@classmethod
	def from_date(
		cls,
		date: datetime
	) -> "StaticGTFS": 
		"""
		Create a StaticGTFS object based on a date - queries the 
		shakeup table and selects the 
		"""
		date_int = StaticGTFSTable.get_int_from_date(date)

		try:
			shakeup = db.session.execute(
				db.select(Shakeup).filter(
					(Shakeup.start_date<date_int)
					& (Shakeup.end_date>=date_int)
				)
			).scalar_one()
		except NoResultFound:
			cls.add_new_static_gtfs()

			try:
				shakeup = db.session.execute(
					db.select(Shakeup).filter(
						(Shakeup.start_date<date_int)
						& (Shakeup.end_date>=date_int)
					)
				).scalar_one()
			except NoResultFound:
				raise ValueError(f"No static data found for date {date}.")

		return cls(shakeup)

	@staticmethod
	def add_new_static_gtfs() -> None:
		"""
		Function to call whenever StaticGTFS detects that it doesn't have 
		up to date static data. 
		"""
		static_url = current_app.config.get("MTS_STATIC_GTFS_URL")
		static_dir = current_app.config.get("STATIC_GTFS_PATH")

		if not isinstance(static_url, str):
			raise ValueError(f"Invalid MTS_STATIC_GTFS_URL {static_url}")

		if not isinstance(static_dir, str):
			raise ValueError(f"Invalid STATIC_GTFS_PATH {static_dir}")

		if static_dir[-1] != '/':
			static_dir += '/'

		shakeup_name = datetime.now().strftime("%b%y")
		shakeup_dir = f"{static_dir}{shakeup_name}/"

		if not os.path.isdir(shakeup_dir):
			os.makedirs(static_dir, exist_ok = True)
			subprocess.call(
				(
					f"curl -O {static_url} && "
					f"unzip google_transit.zip -d {static_dir}{shakeup_name}/ && "
					f"rm google_transit.zip"
				),
				shell = True
			)

		## Add entry to shakeup table
		feed_info = cast(
			FeedInfoRow, 
				pd.read_csv(
				f"{shakeup_dir}/feed_info.txt"
			).iloc[0,:].to_dict()
		)

		shakeup = Shakeup(
			shakeup_name=shakeup_name,
			start_date=feed_info["feed_start_date"],
			end_date=feed_info["feed_end_date"],
		)

		try:
			db.session.add(shakeup)
			db.session.commit()
		except IntegrityError: 
			hprint(f"Already have a shakeup {shakeup_name}.")
			db.session.rollback()

		shakeup_id = db.session.query(Shakeup).filter(
			Shakeup.shakeup_name == shakeup_name
		).one().shakeup_id

		## Add data from txt files

		try:
			route_data: List[Route] = Route.parse(
				f"{shakeup_dir}/routes.txt", 
				shakeup_id
			)

			service_data: List[Service] = Service.parse(
				f"{shakeup_dir}/calendar.txt", 
				shakeup_id
			)

			service_exception_data: List[ServiceException] = ServiceException.parse(
				f"{shakeup_dir}/calendar_dates.txt", 
				shakeup_id
			)

			shape_data: list[Shape] = Shape.parse(
				f"{shakeup_dir}/shapes.txt",
				shakeup_id
			)

			stop_data: List[Stop] = Stop.parse(
				f"{shakeup_dir}/stops.txt",
				shakeup_id
			)

			stop_time_data: List[StopTime] = StopTime.parse(
				f"{shakeup_dir}/stop_times.txt",
				shakeup_id
			)

			trip_data: List[Trip] = Trip.parse(
				f"{shakeup_dir}/trips.txt",
				shakeup_id
			)

			## Remove stop_time data for trips not being added

			known_trips_d: Dict[int, int] = {trip.trip_id: 1 for trip in trip_data}

			filt_stop_time_data: List[StopTime] = []

			for st in stop_time_data:
				try:
					known_trips_d[st.trip_id]
					filt_stop_time_data.append(st)
				except KeyError:
					continue

			db.session.add_all(route_data)
			db.session.add_all(service_data)
			db.session.add_all(service_exception_data)
			db.session.add_all(shape_data)
			db.session.add_all(stop_data)
			db.session.add_all(filt_stop_time_data)
			db.session.add_all(trip_data)

			db.session.commit()

		except Exception as e:
			db.session.rollback()
			hprint("Database was rolled back because of this error:")
			raise e
		




		












