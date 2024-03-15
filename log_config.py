import logging
from logging.handlers import RotatingFileHandler

# Configure the logger
logger = logging.getLogger('my_application')
logger.setLevel(logging.INFO)

# Create a file handler that logs messages to a file 'app.log'
handler = RotatingFileHandler('app.log', maxBytes=1024*1024*5, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
if logger:
    print('Logger set up.')
else:
    print('Error setting up logger')
if handler:
    print('Handler set up.')
else:
    print('Error setting up handler.')
if formatter:
    print('Formatter set up.')
else:
    print('Error setting up formatter.')