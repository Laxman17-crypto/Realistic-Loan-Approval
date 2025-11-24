import logging
import os
from datetime import datetime

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with timestamp
LOG_FILE = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")

# Custom logger configuration
logging.basicConfig(
    filename=LOG_FILE,
    format="[ %(asctime)s ] [ %(levelname)s ] - %(message)s",
    level=logging.INFO
)

def get_logger(name: str = __name__):
    """
    Returns a logger instance with custom formatting.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger