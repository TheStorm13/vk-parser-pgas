import os

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class ReportWriter:
    """Пишет отчеты в файловую систему."""

    def __init__(self):
        """Инициализирует выходную директорию отчетов."""
        result_path: str = os.path.join(os.getcwd(), "reports")
        os.makedirs(result_path, exist_ok=True)
        self.output_dir = result_path

    def write_report(self, filename: str, content: str):
        """Записывает содержимое отчета в файл.

        Args:
            filename: Имя файла отчета (str).
            content: Содержимое отчета (str).

        Returns:
            None

        """
        file_path = f"{self.output_dir}/{filename}"
        with open(file_path, "w", encoding="utf-8") as report_file:
            report_file.write(content)
        logger.info(f"Content is written to {file_path}")
