from typing import Optional, TypedDict


class FeedInfoRow(TypedDict):
	feed_publisher_name: str
	feed_publisher_url: str
	feed_lang: str
	feed_start_date: int
	feed_end_date: int
	feed_version: str
	feed_contact_email: Optional[str]
	feed_contact_url: Optional[str]

class ServiceRow(TypedDict):
	service_id: str
	monday: int
	tuesday: int
	wednesday: int
	thursday: int
	friday: int
	saturday: int
	sunday: int
	start_date: int
	end_date: int
	service_name: str

class ServiceExceptionRow(TypedDict):
	service_id: str
	date: int
	exception_type: int

class RouteRow(TypedDict):
	route_id: str
	agency_id: str
	route_short_name: str
	route_long_name: str
	route_type: int
	route_url: str
	route_color: str
	route_text_color: str
	route_sort_order: Optional[float]
	network_id: Optional[str]
	direction0_name: Optional[str]
	direction1_name: Optional[str]
	route_group: Optional[str]
	route_pattern1: str
	route_pattern2: Optional[str]

class ShapeRow(TypedDict):
	shape_id: str
	shape_pt_lat: float
	shape_pt_lon: float
	shape_pt_sequence: int
	shape_dist_traveled: float

class StopRow(TypedDict):
	stop_id: str
	stop_code: Optional[float]
	stop_name: str
	stop_desc: Optional[str]
	stop_lat: float
	stop_lon: float
	zone_id: Optional[float]
	stop_url: Optional[str]
	location_type: int
	parent_station: Optional[str]
	wheelchair_boarding: int
	platform_code: Optional[int]
	intersection_code: Optional[str]
	reference_place: Optional[str]
	stop_name_short: str
	stop_place: Optional[str]

class StopTimeRow(TypedDict):
	trip_id: int
	arrival_time: str
	departure_time: str
	stop_id: int
	stop_sequence: int
	stop_headsign: Optional[str]
	pickup_type: int
	drop_off_type: int
	shape_dist_traveled: float
	timepoint: int

class TripRow(TypedDict):
	route_id: str
	service_id: str
	trip_id: int
	trip_headsign: str
	direction_id: int
	block_id: str
	shape_id: str
	wheelchair_accessible: int
	bikes_allowed: int
	direction_name: str
	trip_bikes_allowed: int
	trip_headsign_short: str