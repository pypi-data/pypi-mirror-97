import logging
import logging_loki
import datetime
from microservice_template_core.settings import LoggerConfig, ServiceConfig
from multiprocessing import Queue


logger = None


class VerboseFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, 'traceback'):
            record.traceback = ""
        return True


class VerboseFormatter(logging.Formatter):

    def formatMessage(self, record: logging.LogRecord) -> str:
        base_message = f'{datetime.datetime.now()} - {record.name} - {record.levelname} - {record.message}'
        if hasattr(record, 'exception'):
            base_message = base_message + f'\nException: {getattr(record, "exception")}'
        if hasattr(record, 'traceback'):
            base_message = base_message + f'\nTraceback: {getattr(record, "traceback")}'

        return base_message


def get_logger():
    global logger
    if not logger:
        logger = logging.getLogger(ServiceConfig.SERVICE_NAME)
        logger.setLevel(LoggerConfig.LOG_LEVEL)
        loki_handler = logging_loki.LokiQueueHandler(
            Queue(-1),
            url=f"http://{LoggerConfig.LOKI_SERVER}:{LoggerConfig.LOKI_PORT}/loki/api/v1/push",
            tags={"service": ServiceConfig.SERVICE_NAME},
            # auth=("username", "password"),
            version="1",
        )
        if LoggerConfig.LOGGING_VERBOSE:
            print("Verbose logger initialization")
            console_handler = logging.StreamHandler()
            console_handler.setLevel("DEBUG")
            console_handler.setFormatter(VerboseFormatter())
            logger.addHandler(console_handler)
            logger.addFilter(VerboseFilter())
        logger.addHandler(loki_handler)
        logger.info(
            "Service logger initialization",
            extra={"tags": {"tests": "logger-test"}},
        )
    return logger


if __name__ == '__main__':
    LoggerConfig.LOGGING_VERBOSE = True
    test_logger = get_logger()
    test_logger.critical(
        msg="It's test message to check if logging works",
        extra={
            "tags": {
                "tests": "logger-test",
                "traceback": "Traceback here",
                "exception": "It's test exception"
            }
        }
    )
