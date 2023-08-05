import logging
import os

ENVIRONMENT = os.getenv('PYTHON_ENVIRONMENT', 'development')


def configure_logging(upstream_loggers=None):
    upstream_loggers = [] if upstream_loggers is None else upstream_loggers
    format_str = '%(asctime)s [%(name)s]-{%(processName)s-%(threadName)s} %(levelname)s - %(message)s'
    log_level = logging.WARNING

    global ENVIRONMENT
    if is_staging():
        logging.basicConfig(level=logging.INFO, format=format_str)
        log_level = logging.ERROR
    elif is_production():
        logging.basicConfig(level=logging.WARN, format=format_str)
        log_level = logging.ERROR
    elif is_development():
        logging.basicConfig(level=logging.DEBUG, format=format_str)
    else:
        logging.basicConfig(level=logging.DEBUG, format=format_str)
        ENVIRONMENT = 'Development'

    for logger in upstream_loggers:
        logging.getLogger(logger).setLevel(log_level)


def is_development():
    return ENVIRONMENT.lower() == 'development'


def is_staging():
    return ENVIRONMENT.lower() == 'staging'


def is_production():
    return ENVIRONMENT.lower() == 'production'
