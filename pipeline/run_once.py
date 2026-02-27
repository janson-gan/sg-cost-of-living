from utils.logger import logger
from utils.db import test_connection
from datetime import datetime
from extractors.hdb_extractor import extract_hdb
from extractors.coe_extractor import extract_coe
from extractors.cpi_extractor import extract_cpi
from loaders.raw_loader import load_raw

"""
This is a manual pipeline trigger to test extract and load raw data
Run this during development phase to test the pipeline
python run_once.py
"""


def run_pipeline_once():
    # Records the current timestamp when pipeline start
    start_time = datetime.now()
    batch_id = start_time.strftime("%Y%M%d_%H%M%S")

    logger.info("=" * 50)
    logger.info("Manual pipeline run")
    logger.info(f"Batch ID: {batch_id}")
    logger.info("=" * 50)

    # Test database connection before extract and load work
    test_connection()

    # -- Extract data --
    logger.info("")
    logger.info("-" * 40)
    logger.info("Extracting Data")
    logger.info("-" * 40)

    # Store each extract function to a specific variable
    hdb_records = extract_hdb()
    coe_records = extract_coe()
    cpi_records = extract_cpi()

    # -- Load Raw Data --
    logger.info("")
    logger.info("-" * 40)
    logger.info("Load Raw Data")
    logger.info("-" * 40)

    hdb_count = load_raw(hdb_records, "hdb_resale", batch_id)
    coe_count = load_raw(coe_records, "coe_results", batch_id)
    cpi_count = load_raw(cpi_records, "cpi_data", batch_id)

    # Summary
    elapsed = datetime.now() - start_time

    logger.info("")
    logger.info("=" * 60)
    logger.info("Pipeline Complete")
    logger.info(f"  HDB records loaded:  {hdb_count:,}")
    logger.info(f"  COE records loaded:  {coe_count:,}")
    logger.info(f"  CPI records loaded:  {cpi_count:,}")
    logger.info(f"  Total time:          {elapsed}")
    logger.info(f"  Batch ID:            {batch_id}")
    logger.info("=" * 60)


# Ensure run pipeline start only when the script is run directly
# Prevent others program accidentally run it.
if __name__ == "__main__":
    run_pipeline_once()
