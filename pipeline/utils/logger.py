from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss!UTC+8} | {level: <8} | {message}",
    level="INFO",
)

logger.add(
    "logs/pipeline_{time: YYYY-MM-DD}.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
)