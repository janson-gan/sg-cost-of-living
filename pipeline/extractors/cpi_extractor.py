from extractors.api_client import fetch_all_records
from utils.logger import logger
import os

resource_id = os.environ.get("DATAGOV_CPI_RESOURCE_ID")


def extract_cpi():
    """
    Fetches all CPI records from Data.gov.sg.
    Return list of dictionaries, with each representing one CPI data point.
    """
    logger.info("Extracting CPI data...")
    records = fetch_all_records(resource_id, "CPI Data")
    return records
