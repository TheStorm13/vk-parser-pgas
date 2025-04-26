from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class ReportWriter:
    def __init__(self, output_dir: str):
        """
        Initialize the ReportWriter with the given output directory.
        """
        self.output_dir = output_dir

    def write_report(self, filename: str, content: str):
        file_path = f"{self.output_dir}/{filename}"  # Build full file path
        with open(file_path, "w", encoding="utf-8") as report_file:
            report_file.write(content)  # Write content to file
        logger.info(f"Content is written to {file_path}")  # Log the file path
