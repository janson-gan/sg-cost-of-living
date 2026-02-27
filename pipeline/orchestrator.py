import schedule
import time
from datetime import datetime
from utils.logger import logger
from utils.db import test_connection
from extractors.hdb_extractor import extract_hdb
from extractors.coe_extractor import extract_coe
from extractors.cpi_extractor import extract_cpi
from loaders.raw_loader import load_raw

# This function run the pipeline once a day


def run_pipeline():
    # Records the current timestamp when pipeline start
    start_time = datetime.now()
    # Create a batch id for traceability
    batch_id = start_time.strftime("%Y%M%d_%H%M%S")

    # Log start with batch id
    logger.info("=" * 60)
    logger.info("🔄 Scheduled Pipeline Run")
    logger.info(f"📋 Batch ID: {batch_id}")
    logger.info("=" * 60)

    try:
        # Extract data with three extractors
        hdb_records = extract_hdb()
        coe_records = extract_coe()
        cpi_records = extract_cpi()

        # Load raw into its own table with batch id
        hdb_count = load_raw(hdb_records, "hdb_resale", batch_id)
        coe_count = load_raw(coe_records, "coe_results", batch_id)
        cpi_count = load_raw(cpi_records, "cpi_data", batch_id)

        # Summary of records loaded and timestamp
        elapsed = datetime.now() - start_time
        logger.info("=" * 60)
        logger.info("Scheduled Pipeline Complete")
        logger.info(
            f"  HDB: {hdb_count:,} | COE: {coe_count:,} | CPI: {cpi_count:,}")
        logger.info(f"  Duration: {elapsed}")
        logger.info("=" * 60)

    # Catch and log the error if pipeline failed
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

# Scheduler setup
def main():
    logger.info("=" * 50)
    logger.info("SG Cost of Living - ETL Pipeline")
    logger.info("=" * 50)

    # Test database connection
    test_connection()

    # Pipeline run evey day at 2.00am
    schedule.every().day.at("02:00").do(run_pipeline)

    logger.info("Pipeline schedule: daily at 02:00 SGT")
    logger.info("Waiting for next schedule run...")

    # Infinite loop for checking the time for running pipeline
    while True:
        schedule.run_pending()
        time.sleep(60)


# Ensure scheduler start only when the script is run directly
# Prevent others program accidentally run it.
if __name__ == "__main__":
    main()
