import schedule
import time
from utils.logger import logger
from utils.db import test_connection

def run_pipeline():
    logger.info("Pipeline triggered - ETL jobs coming on Phase 2")

def main():
    logger.info("=" * 50)
    logger.info("SG Cost of Living - ETL Pipeline")
    logger.info("=" * 50)

    test_connection()

    schedule.every().day.at("02:00").do(run_pipeline)

    logger.info("Pipeline schedule: daily at 02:00 SGT")
    logger.info("Waiting for next schedule run...")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()