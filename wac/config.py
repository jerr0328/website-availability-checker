import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

KAFKA_ENDPOINT = os.getenv("KAFKA_ENDPOINT")
KAFKA_CERT_DIR = os.getenv("KAFKA_CERT_DIR", "./certs")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "website-monitoring")
KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "website-monitoring-client")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "website-monitoring-group")
KAFKA_USE_SSL = os.getenv("KAFKA_USE_SSL", "true").lower() != "false"
CHECK_TIMEOUT = float(os.getenv("CHECK_TIMEOUT", "1"))
POSTGRES_ENDPOINT = os.getenv("POSTGRES_ENDPOINT")
