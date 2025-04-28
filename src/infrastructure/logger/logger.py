import logging
from logging.handlers import RotatingFileHandler


def setup_logger(
    name: str, log_file: str = "app.log", level: int = logging.INFO
) -> logging.Logger:
    """
    Setup and configure a logger with both console and rotating file handlers.

    :param name: Name of the logger, typically the module name.
    :param log_file: Path to the log file. Defaults to 'app.log'.
    :param level: Logging level. Defaults to logging.INFO.
    :return: Configured logger instance.
    """

    logger = logging.getLogger(name)  # Get or create a logger by name
    logger.setLevel(level)  # Set logging level

    if logger.hasHandlers():
        # Clear existing handlers to prevent duplicate logs
        logger.handlers.clear()

    # Define a uniform log format
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Setup console handler with the log formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Setup rotating file handler for file-based logging

    # file_handler = RotatingFileHandler(
    #     log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    # )
    # file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    return logger  # Return the configured logger instance
