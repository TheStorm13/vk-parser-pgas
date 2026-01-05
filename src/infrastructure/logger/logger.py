import logging


def setup_logger(
        name: str, log_file: str = "app.log", level: int = logging.INFO,
) -> logging.Logger:
    """Создает настроенный logger с консольным и опциональным файловым логированием.

    Args:
        name: Имя логгера.
        log_file: Путь к файлу лога.
        level: Уровень логирования.

    Returns:
        logging.Logger: Экземпляр логгера.

    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        # Сбрасывает обработчики, чтобы исключить дублирование записей
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Ротационный файловый лог отключен; раскомментируйте при необходимости
    # from logging.handlers import RotatingFileHandler
    # file_handler = RotatingFileHandler(
    #     log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    # )
    # file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    return logger
