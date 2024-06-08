from flask import Flask
import os

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

@app.route('/')
def index():
	secret_key = app.config.get("MTS_API_KEY")
	if secret_key is None:
		raise ValueError("Missing API key for MTS live feed")

	return f"Length of secret key is {len(secret_key)}"

