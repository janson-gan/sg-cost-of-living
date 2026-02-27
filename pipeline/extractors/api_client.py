import requests
import time
from utils.logger import logger
from utils.config import DATAGOV_BASE_URL
from utils.config import DATAGOV_API_KEY

# Function to fetch all records from Data.gov.sg API


def fetch_all_records(resource_id, dataset_name="dataset"):
    # Empty list to store all records
    all_records = []
    # Start from the very first page of the dataset
    offset = 0
    # Maximum record per page
    limit = 2000
    # Pause between successful requests
    delay_between_requests = 8
    # Maximum retries if errors occur
    max_retries = 5

    # Set API key if available
    headers = {}
    if DATAGOV_API_KEY:
        headers["Authorization"] = f"Bearer{DATAGOV_API_KEY}"

    logger.info(f"Starting extraction: {dataset_name}")

    while True:
        # Track numner of retries
        retries = 0
        # Track if the batch was fetched
        success = False

        # Run loop until all records are fetched or reach maximum retries
        while retries < max_retries and not success:
            try:
                # Get request to Data.gov.sg with parameters
                response = requests.get(
                    DATAGOV_BASE_URL,
                    params={
                        "resource_id": resource_id,
                        "offset": offset,
                        "limit": limit
                    },
                    headers=headers,
                    # wait for 30 seconds for the response
                    timeout=30
                )

                # Check response return status code 429 (too many requests)
                if response.status_code == 429:
                    # add 1 to retries if response return status code 429
                    retries += 1
                    # Exponential backoff wait time
                    # 10s, 20s, 40s, 80s, 160s
                    wait_time = 10 * (2 ** (retries - 1))
                    logger.warning(
                        f"Rate limited on: {dataset_name}."
                        f"Retry {retries}/{max_retries} in {wait_time}s..."
                    )
                    # Sleep before retrying request
                    time.sleep(wait_time)
                    continue

                # return a error if Http status code not 200
                response.raise_for_status()

                # convert the response to JSON format
                data = response.json()

                # Check payload if success is true. If not, log error message and stop
                if not data.get("success"):
                    logger.error(f"API return success=fail: {dataset_name}")
                    break

                # Extract records the actual data rows
                records = data["result"]["records"]

                # Total number of records in the dataset
                total = data["result"]["total"]

                # Add new records to all_records
                all_records.extend(records)

                # Log the fetching progress, the numbers of records fetched vs total
                # :, format the numbers with commas: 10000 -> 10,000
                logger.info(
                    f"Fetched {len(all_records):,} / {total:,} records"
                    f"(offset={offset})"
                )

                # Cool down for 15s after recovered from rate limit
                if retries > 0:
                    logger.info(
                        f"Cooling down for 15s after rate limit recovery...")
                    time.sleep(15)

                # Increase the offset by the limit (move to next batch)
                offset += limit
                success = True

                # Break the loop if offset is equal or greater than the total (all records fetched)
                if offset >= total:
                    break

                # Sleep before the next request
                time.sleep(delay_between_requests)

            # If timeout error, increase 1 to retries, raise error, and wait for 10s before retrying
            except requests.exceptions.Timeout:
                retries += 1
                logger.warning(
                    f"Timeout on {dataset_name} at offset: {offset}"
                    f"Retry {retries}/{max_retries}..."
                )
                time.sleep(10)

            # Catch any type of error and stop fetching
            # If error due to rate limit (429), increase 1 to retries, and start waiting time (exponential backoff)
            # before retrying
            except requests.exceptions.RequestException as e:
                if "429" not in str(e):
                    logger.error(f"Request failed for {dataset_name}: {e}")
                    return all_records
                retries += 1
                wait_time = 10 * (2 ** (retries - 1))
                logger.warning(
                    f"Rate limit on {dataset_name}."
                    f"Retry {retries}/{max_retries} in {wait_time}s..."
                )
                time.sleep(wait_time)

        # If attempt reach max retries, log error and stop the process.
        # return all data
        if retries >= max_retries:
            logger.error(
                f"Max retries reached for {dataset_name} at offset: {offset}."
                f"Returning {len(all_records):,} records fetched so far."
            )
            break

        # If offset matched or exceeded total, stop process
        if offset >= total:
            break
    # Log the completed extraction with total records fetched
    logger.info(
        f"Extraction completed: {dataset_name} "
        f"{len(all_records):,} total records"
    )
    # Return the result
    return all_records
