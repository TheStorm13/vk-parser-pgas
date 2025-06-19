from pathlib import Path
import sys
import logging
from typing import Optional

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)

class AppResources:
    """Handles application resources and file operations"""

    def __init__(self):
        self._base_path = self._get_base_path()

    def _get_base_path(self) -> Path:
        """Get correct base path for both development and bundled app"""
        if getattr(sys, 'frozen', False):  # For PyInstaller, Nuitka
            return Path(sys._MEIPASS)
        return Path.cwd()

    def get_resource(self, relative_path: str) -> Path:
        """Get absolute path to resource"""
        return self._base_path / relative_path

    def read_text_file(self, relative_path: str) -> Optional[str]:
        """
        Safely read text file with error handling
        Returns content if successful, None otherwise
        """
        file_path = self.get_resource(relative_path)

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.is_file():
                raise IOError(f"Not a file: {file_path}")
            if not file_path.access(Path.R_OK):
                raise PermissionError(f"No read permissions: {file_path}")

            return file_path.read_text(encoding='utf-8')

        except Exception as e:
            logger.error(f"Failed to read {file_path}: {str(e)}")
            return None
