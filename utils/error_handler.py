import logging

def handle_error(exception):

    logger = logging.getLogger(__name__)
    logger.error("An error occurred: %s", exception, exc_info=True)