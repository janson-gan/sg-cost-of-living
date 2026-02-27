from extractors.api_client import fetch_all_records
from utils.logger import logger
import os

resource_id = os.environ.get("DATAGOV_COE_RESOURCE_ID")


def extract_coe():
    """
    Fetches all COE bidding results from Data.gov.sg.
    Return list of dictionaries, with each representing one bidding result.
    """
    logger.info("Extracting COE data...")
    records = fetch_all_records(resource_id, "COE Results")
    return records
