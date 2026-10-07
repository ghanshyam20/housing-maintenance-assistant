import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/maintenance.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_action(request_id, action):
    logging.info("%s - %s", request_id, action)
