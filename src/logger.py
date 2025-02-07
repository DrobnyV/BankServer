import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("bank_system.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("BankLogger")
