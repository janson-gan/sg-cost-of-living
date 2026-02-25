import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "sg_cost_living"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "")
}

DATAGOV_BASE_URL = os.environ.get(
    "DATAGOV_BASE_URL",
    "https://data.gov.sg/api/action/datastore+search",
)