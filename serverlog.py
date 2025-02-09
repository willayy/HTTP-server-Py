from datetime import datetime
import logging
import os

def init_logging():
    # Create a folder called logs if it doesn't exist
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Get the current day
    start_time = datetime.now()
    log_date = start_time.strftime("%Y-%m-%d")

    # Create a logger for the day
    logging.basicConfig(
        filename=f"logs/{log_date}_server.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def log_info(message: str): logging.info(message)
def log_error(message: str): logging.error(message)
def log_warning(message: str): logging.warning(message)
    