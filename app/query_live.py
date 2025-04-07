from flask_sqlalchemy import SQLAlchemy
from app.models.live import LiveRecord, Query
from google.transit import gtfs_realtime_pb2
import requests
import time
import datetime
import sys

from utils import hprint


def query_live(
	db: SQLAlchemy,
	endpoint: str,
	api_key: str
) -> None:
	"""
	Given a connected database and and parameters for
	a GTFS feed, queries the feed and inserts all current
	records into the live table

	Parameters
	----------
	db : flask_sqlalchemy.SQLAlchemy
		The `db` instance created by `app`. 
	endpoint : str
		The GTFS live feed URL
	api_key : str
		API key for the database
	"""
	feed = gtfs_realtime_pb2.FeedMessage() #type: ignore

	tries = 0
	sleep_times = {0: 1, 1: 3, 2: 5}

	while True:
		try:
			response = requests.get(endpoint+"?key="+api_key)
			tries = 0
			break
		except requests.exceptions.ConnectionError:
			try:
				time_to_sleep = sleep_times[tries]
			except KeyError:
				hprint(f"Failed to maintain live feed connection after {tries+1} attempts. Abandoning this sample.")
				return None

			hprint(f"Failed to maintain live feed connection. Sleeping {time_to_sleep} seconds before trying again.")
			time.sleep(time_to_sleep)
			tries += 1


	feed.ParseFromString(response.content)

	new_query = Query(
		query_id = None,
		live_feed_timestamp = int(feed.entity[0].trip_update.timestamp),
		records = []
	)

	db.session.add(new_query)
	db.session.commit()

	for entity in feed.entity:
		new_rec = LiveRecord(
			rec_id = None,
			trip_id = entity.trip_update.trip.trip_id,
			next_stop_id = int(entity.trip_update.stop_time_update[0].stop_id),
			next_stop_departure = None,
			vehicle_id = int(entity.trip_update.vehicle.id),
			raw_delay = None,
			query = new_query,
			query_id = new_query.query_id
		)

		if new_rec.vehicle_id < 100:
			## This is a trolley. They give their own delay measurements, 
			## not next stop departures.
			new_rec.raw_delay = int(entity.trip_update.delay) // 60
		else:
			## This is a bus. They don't populate the delay field, they
			## use next stop estimated departures
			new_rec.next_stop_departure = (int(
				entity.trip_update.stop_time_update[0].departure.time
			) - new_query.live_feed_timestamp)
			

		db.session.add(new_rec)
		db.session.commit()

	hprint(f"Retrieved {len(feed.entity)} vehicle records at {datetime.datetime.now().strftime('%I:%M%p')}")

	return None




