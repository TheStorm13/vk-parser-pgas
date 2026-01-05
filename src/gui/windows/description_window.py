import tkinter as tk
from pathlib import Path
from tkinter import ttk

from markdown import markdown
from tkhtmlview import HTMLLabel

from src.gui.styles import Styles
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.storage.app_resources import AppResources

logger = setup_logger(__name__)


class DescriptionWindow(tk.Toplevel):
    """Отображает описание приложения в скроллируемом окне."""

    def __init__(self, parent):
        """Инициализирует окно описания.

        Args:
            parent: Родительское окно Tk.

        Returns:
            None

        """
        super().__init__(parent)
        self.title("Описание")
        self.configure(bg="white")
        self.resizable(True, False)
        self.geometry("600x600")
        self.minsize(100, 100)
        self.maxsize(800, 800)

        self.style = Styles.configure_styles(self)

        resources = AppResources()
        description = resources.read_text_file("data/description_app.md")

        html_content = markdown(description)
        html_content = f"""<div style="font-size: 12px;">{html_content}</div>"""

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.html_label = HTMLLabel(
            self.main_frame, html=html_content, background="white", width=50, height=20,
        )
        self.html_label.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.html_label.yview,
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.html_label.configure(yscrollcommand=self.scrollbar.set)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, pady=(10, 10), sticky="ew")
        button_frame.columnconfigure(0, weight=1)

        close_button = ttk.Button(
            button_frame, text="Закрыть", command=self.destroy, style="Accent.TButton",
        )
        close_button.grid(row=0, column=0)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """Сохраняет позицию прокрутки при изменении размера окна.

        Args:
            event: Событие Tkinter.

        Returns:
            None

        """
        current_scroll = self.html_label.yview()[
            0
        ]  # Получает текущую позицию вертикальной прокрутки
        self.update()

        # Восстанавливает позицию прокрутки после ресайза
        self.after(10, lambda: self.html_label.yview_moveto(current_scroll))

    def read_description_file(file_path: Path) -> str:
        """Читает файл описания.

        Args:
            file_path: Путь к файлу.

        Returns:
            Содержимое файла или ошибку.

        """
        path = Path(file_path) if isinstance(file_path, str) else file_path

        if not path.exists():
            error_msg = f"Error: File not found - {path}"
            logger.warning(error_msg)
            return error_msg

        if not path.is_file():
            error_msg = f"Error: Not a file - {path}"
            logger.warning(error_msg)
            return error_msg

        if not path.access(Path.R_OK):  # Проверяет права на чтение
            error_msg = f"Error: No read permissions - {path}"
            logger.warning(error_msg)
            return error_msg

        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            error_msg = f"Error: File is not UTF-8 encoded - {path}"
            logger.warning(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error while reading file: {e!s}"
            logger.warning(error_msg)
            return error_msg
