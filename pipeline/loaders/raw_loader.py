import json
from datetime import datetime
from utils.db import get_connection
from utils.logger import logger

# Function to load raw data into PostgreSQL table in batches
# Take a list of extracted records, insert into table with batch id


def load_raw(records, table_name, batch_id=None):

    # If empty records, log error and return
    if not records:
        logger.warning(f"No records to load into raw_data. {table_name}")
        return 0

    # If no batch id, set current date time into batch id, e.g., 20260226_115700
    if batch_id is None:
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Open the DB connection and cursor
    conn = get_connection()
    cursor = conn.cursor()
    # To track how many records are inserted
    inserted = 0

    try:
        # SQL statement
        # Insert a row into a table with two values, source data and batch id
        # %s is a placeholder for actual values, to prevent SQL injection and hard-coding values.
        insert_sql = f"""
            INSERT INTO raw_data.{table_name} (source_data, batch_id)
            VALUES(%s, %s)
        """

        # Define number of records to be inserted
        batch_size = 1000

        # Batch insert loop
        # Loop through the list of records in steps of batch size
        for i in range(0, len(records), batch_size):
            # Break huge records into smaller batch in term of batch size in each loop
            batch = records[i:i + batch_size]
            # Convert each record in the batch to JSON format with batch id
            batch_data = [
                (json.dumps(record), batch_id)
                for record in batch
            ]
            # Executive the SQL query and insert the batch data into database
            cursor.executemany(insert_sql, batch_data)
            # Count the number of inserted batch data
            inserted += len(batch)

            logger.info(
                f"Loaded {inserted:,} / {len(records):,} "
                f"into raw_table.{table_name}"
            )
            # To save each batch data to the database permanently
            conn.commit()

            logger.info(
                f"Loaded {inserted:,} records into "
                f"raw_data.{table_name} (batch: {batch_id})"
            )
    # If anything fail, roll back the transaction (insert, update, delete) and log the error
    # Ensure database goes back to the state before the transaction
    # Prevent incomplete or corrupted data
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to load raw_data.{table_name}: {e}")
        # Re-raise the error to show awareness of the failure
        raise

    # Close all connections even if an error occur
    # Prevent resource leak
    finally:
        cursor.close()
        conn.close()
        logger.info("PostgreSQL connection closed.")
    # Return the total number of successful inserted records
    return inserted
