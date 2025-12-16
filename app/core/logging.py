import logging
from pythonjsonlogger import jsonlogger

def setup_logging(level: str = "INFO"):
    logger = logging.getLogger()
    logger.setLevel(level)

    # avoid duplicate handlers in reload
    if logger.handlers:
        return

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
