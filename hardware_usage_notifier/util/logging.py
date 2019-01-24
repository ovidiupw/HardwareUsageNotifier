import datetime
import logging
import sys
import uuid
import os

DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p %Z'
TRACE_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
SIMPLE_LOG_FORMAT = '%(asctime)s - %(message)s'
LOG_FILE_EXTENSION = 'log'
LOGGER_ID = 'Logger'


def build_production_logger(logger_name=__name__):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    file_log_handler = logging.FileHandler(
        filename=f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')}.{uuid.uuid4()}.{LOG_FILE_EXTENSION}",
        mode='w')
    file_log_handler.setLevel(logging.DEBUG)
    file_log_formatter = logging.Formatter(
        fmt=TRACE_LOG_FORMAT,
        datefmt=DATE_FORMAT)

    console_log_handler = logging.StreamHandler(
        stream=sys.stdout)
    console_log_handler.setLevel(logging.INFO)
    console_log_formatter = logging.Formatter(
        fmt=SIMPLE_LOG_FORMAT,
        datefmt=DATE_FORMAT)

    file_log_handler.setFormatter(file_log_formatter)
    console_log_handler.setFormatter(console_log_formatter)

    logger.addHandler(file_log_handler)
    logger.addHandler(console_log_handler)

    return logger


def build_test_logger(logger_name=__name__):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    console_log_handler = logging.StreamHandler(
        stream=sys.stdout)
    console_log_handler.setLevel(logging.INFO)
    console_log_formatter = logging.Formatter(
        fmt=TRACE_LOG_FORMAT,
        datefmt=DATE_FORMAT)

    console_log_handler.setFormatter(console_log_formatter)

    logger.addHandler(console_log_handler)

    return logger


def shut_down_loggers():
    logging.shutdown()


def cleanup_empty_log_files(directory):
    # print('Cleaning up empty log files...')
    for file_name in os.listdir(directory):
        if os.path.isfile(file_name):
            try:
                if file_name.endswith(LOG_FILE_EXTENSION) and os.path.getsize(file_name) == 0:
                    # print(f"Found empty log file '{file_name}'. Trying to remove it.")
                    os.remove(file_name)
            except OSError as e:
                # print(f"Could not delete empty file '{file_name}': {e.args[0]}")
                pass
