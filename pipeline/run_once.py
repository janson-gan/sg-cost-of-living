from utils.logger import logger
from utils.db import test_connection

def run_pipeline_once():
    logger.info("=" * 50)
    logger.info("Manual pipeline run")
    logger.info("=" * 50)

    test_connection()

    logger.info("Pipeline run complete (ETL steps coming Phase 2)")

if __name__ == "__main__":
    run_pipeline_once()