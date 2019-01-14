import datetime
import logging
import sys
import uuid

DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p %Z'
TRACE_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
SIMPLE_LOG_FORMAT = '%(asctime)s - %(message)s'


def build_production_logger(logger_name=__name__):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    file_log_handler = logging.FileHandler(
        filename=f"{datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%SZ')}.{uuid.uuid4()}.log",
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
