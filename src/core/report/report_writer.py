import os

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class ReportWriter:
    def __init__(self):
        """
        Initialize the ReportWriter with the given output directory.
        """
        result_path: str = os.path.join(os.getcwd(), "reports")  # Папка reports в корне приложения
        os.makedirs(result_path, exist_ok=True)  # Создать папку, если она не существует

        self.output_dir = result_path

    def write_report(self, filename: str, content: str):
        file_path = f"{self.output_dir}/{filename}"  # Build full file path
        with open(file_path, "w", encoding="utf-8") as report_file:
            report_file.write(content)  # Write content to file
        logger.info(f"Content is written to {file_path}")  # Log the file path
