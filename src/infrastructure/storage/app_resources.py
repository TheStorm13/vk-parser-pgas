import os
import sys
from pathlib import Path

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class AppResources:
    """Управляет ресурсами и файловыми операциями."""

    def __init__(self):
        self._base_path = self._get_base_path()

    def _get_base_path(self) -> Path:
        """Определяет базовый путь для разработки и сборки.

        Returns:
            Path: Базовый путь.

        """
        if getattr(sys, "frozen", False):  # Для PyInstaller, Nuitka
            return Path(sys._MEIPASS)
        return Path.cwd()

    def get_resource(self, relative_path: str) -> Path:
        """Возвращает абсолютный путь к ресурсу.

        Args:
            relative_path (str): Относительный путь.

        Returns:
            Path: Абсолютный путь к ресурсу.

        """
        return self._base_path / relative_path

    def read_text_file(self, relative_path: str) -> str | None:
        """Безопасно читает текстовый файл.

        Args:
            relative_path (str): Относительный путь.

        Returns:
            str | None: Текст файла или None.

        """
        file_path = self.get_resource(relative_path)

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.is_file():
                raise OSError(f"Not a file: {file_path}")
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"No read permissions: {file_path}")

            return file_path.read_text(encoding="utf-8")

        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e!s}")
            return None
