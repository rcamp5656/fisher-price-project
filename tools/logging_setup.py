# tools/logging_setup.py
import os, logging

script_dir = os.path.dirname(os.path.realpath(__file__))
log_path   = os.path.join(script_dir, 'log.txt')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    fh = logging.FileHandler(log_path, mode='w')
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

logger.info("Application start")
