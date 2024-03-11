import os

API_AUTH_TOKEN = os.environ["API_AUTH_TOKEN"]
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

DB = {
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "name": os.environ["DB_NAME"],
}
