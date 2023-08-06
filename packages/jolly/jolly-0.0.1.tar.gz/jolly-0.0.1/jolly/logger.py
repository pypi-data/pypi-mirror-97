import sys
from logging import INFO, FileHandler, StreamHandler, getLogger
from jolly.definitions import jolly
from jolly.env import is_prod

# Create Jolly logger.
logger = getLogger(jolly)
logger.addHandler(StreamHandler(sys.stdout) if is_prod() else FileHandler('{}.log'.format(jolly)))
logger.setLevel(INFO)