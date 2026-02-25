import psycopg2
from utils.config import DB_CONFIG
from utils.logger import logger

def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW() AT TIME ZONE 'Asia/Singapore'")
        now = cur.fetchone()[0]
        logger.info(f"Connected to PostgreSQL. DB time (SGT): {now}")
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"PostgreSQL connection failed: {e}")
        raise