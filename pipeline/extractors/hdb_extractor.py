from extractors.api_client import fetch_all_records
from utils.logger import logger
import os

resource_id = os.environ.get("DATAGOV_HDB_RESOURCE_ID")


def extract_hdb():
    """
    Fetches all HDB records from Data.gov.sg.
    Return list of dictionaries, with each representing one transaction.
    Example:
    {
        "month": "2017-01",
        "town": "ANG MO KIO",
        "flat_type": "2 ROOM",
        "block": "406",
        "street_name": "ANG MO KIO AVE 10",
        ...
    }
    """
    logger.info("Extracting HDB data...")
    records = fetch_all_records(resource_id, "HDB Resale")
    return records
