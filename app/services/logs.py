import picologging as logging
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
logging_folder = os.path.join(root_path, "LOGs")
os.makedirs(logging_folder, exist_ok=True)

log_file_path = os.path.join(logging_folder, "PROXERA.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)