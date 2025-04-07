from flask import Flask
from flask_migrate import Migrate
from config import Config, DevelopmentConfig, ProductionConfig
import threading
import time
import os

from app.extensions import db
from app.query_live import query_live
from app.models.StaticGTFS import StaticGTFS
from utils import hprint


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	## Flask extensions
	db.init_app(app)
	migrate = Migrate(app, db)

	## Register blueprints
	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	## For eventually making more than one blueprint, 
	## see https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy

	## Initiate live database population
	## Attempting simple solution since Celery might be overkill
	## Simpler instructions here: https://tiagohorta1995.medium.com/python-flask-api-background-task-96bf1120a855
	endpoint = app.config.get("MTS_LIVE_ENDPOINT")
	if not isinstance(endpoint, str):
		raise ValueError("Missing MTS_LIVE_ENDPOINT in config")

	api_key = app.config.get("MTS_API_KEY")
	if not isinstance(api_key, str):
		raise ValueError("Missing MTS_API_KEY in config")

	def query_thread_target() -> None:
		while True:
			with app.app_context():
				query_live(
					db,
					endpoint,
					api_key
				)

			time.sleep(60)

	if app.config.get("QUERY_LIVE"):
		live_thread = threading.Thread(target=query_thread_target)
		live_thread.start()
	else:
		hprint("Running application without sampling the live feed")

	return app

config_name = os.environ.get("APP_SETTINGS")

if config_name is None or config_name == "Config.Config":
	app = create_app()
elif config_name == "config.ProductionConfig":
	app = create_app(ProductionConfig)
elif config_name == "Config.DevelopmentConfig":
	app = create_app(DevelopmentConfig)
else:
	raise ValueError(f"Requested config class '{config_name}' not found.")