# logger.py
import logging
import os
from datetime import datetime

if not os.path.exists('logs'):
    os.makedirs('logs')

log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


logger = logging.getLogger('rag bdnd')
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
