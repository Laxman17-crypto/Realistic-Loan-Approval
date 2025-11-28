import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = f"{LOG_DIR}/app_{datetime.now().strftime('%Y_%m_%d')}.log"

logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger("loan_approval")