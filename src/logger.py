import logging

LOGGER = logging.getLogger("Default")

fh = logging.FileHandler("logging.log")
LOGGER.setLevel(logging.DEBUG)
fh.setLevel(logging.INFO)
LOGGER.addHandler(fh)
