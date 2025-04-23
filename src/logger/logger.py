import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str = "app.log", level: int = logging.INFO) -> logging.Logger:
    """
    Создаёт и настраивает логгер с ротацией файлов и выводом в консоль.
    
    :param name: Имя логгера (напр. имя текущего модуля).
    :param log_file: Путь к файлу логов.
    :param level: Уровень логирования. Пример: logging.INFO, logging.DEBUG.
    :return: Настроенный объект логгера.
    """
    # Создаём логгер с указанным именем
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверяем, чтобы хэндлеры не дублировались
    if logger.hasHandlers():
        logger.handlers.clear()

    # Форматирование логов
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Логирование в файл с ротацией
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3,
                                       encoding="utf-8")  # 5MB на файл
    file_handler.setFormatter(formatter)

    # Добавляем хэндлеры в логгер
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
