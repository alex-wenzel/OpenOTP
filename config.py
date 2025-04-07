import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	DEBUG = False
	DEVELOPMENT = False
	MTS_API_KEY = os.getenv("MTS_API_KEY")
	MTS_LIVE_ENDPOINT = os.getenv("MTS_LIVE_ENDPOINT")
	SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
	MTS_STATIC_GTFS_URL = "https://www.sdmts.com/google_transit_files/google_transit.zip"
	STATIC_GTFS_PATH = "./mts_static_gtfs/"
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	QUERY_LIVE = False

class ProductionConfig(Config):
	QUERY_LIVE = True

class StagingConfig(Config):
	DEVELOPMENT = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
