import os

class Config:
	DEBUG = False
	DEVELOPMENT = False
	MTS_API_KEY = os.getenv("MTS_API_KEY")

class ProductionConfig(Config):
	pass

class StagingConfig(Config):
	DEVELOPMENT = True

class DevelopmentConfig(Config):
	DEVELOPMENT = True
	DEBUG = True
