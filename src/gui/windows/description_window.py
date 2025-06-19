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
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Описание")
        self.configure(bg="white")
        self.resizable(True, False)
        self.geometry("600x600")
        self.minsize(100, 100)
        self.maxsize(800, 800)

        # Configure styles for the window (defined in external Styles module)
        self.style = Styles.configure_styles(self)

        # Read description file
        resources = AppResources()
        description = resources.read_text_file("data/description_app.md")

        # Convert Markdown content to HTML
        html_content = markdown(description)
        html_content = f"""<div style="font-size: 12px;">{html_content}</div>"""

        # Main frame containing the HTML content
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Render the description as HTML
        self.html_label = HTMLLabel(
            self.main_frame, html=html_content, background="white", width=50, height=20
        )
        self.html_label.grid(row=0, column=0, sticky="nsew")

        # Adding a vertical scrollbar tied to the HTML label
        self.scrollbar = ttk.Scrollbar(
            self.main_frame, orient="vertical", command=self.html_label.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Sync scrollbar with HTML label's scroll movement
        self.html_label.configure(yscrollcommand=self.scrollbar.set)

        # Frame for a close button
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, pady=(10, 10), sticky="ew")
        button_frame.columnconfigure(0, weight=1)

        # Button to close the window
        close_button = ttk.Button(
            button_frame, text="Закрыть", command=self.destroy, style="Accent.TButton"
        )
        close_button.grid(row=0, column=0)

        # Configure layout weights for resizing behavior
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Handle window resizing to maintain scroll position
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """
        Keep the current scroll position when the window is resized.
        """
        current_scroll = self.html_label.yview()[
            0
        ]  # Get current vertical scroll position
        self.update()

        # After resizing, restore the scroll position
        self.after(10, lambda: self.html_label.yview_moveto(current_scroll))

    def read_description_file(file_path: Path) -> str:
        """
        Читает файл с описанием приложения.
        Возвращает содержимое файла или строку с ошибкой, если что-то пошло не так.

        Args:
            file_path (str | Path): Путь к файлу (строка или объект Path).

        Returns:
            str: Содержимое файла или сообщение об ошибке.
        """
        path = Path(file_path) if isinstance(file_path, str) else file_path

        # Проверка существования и доступности файла
        if not path.exists():
            error_msg = f"Error: File not found - {path}"
            logger.warning(error_msg)
            return error_msg

        if not path.is_file():
            error_msg = f"Error: Not a file - {path}"
            logger.warning(error_msg)
            return error_msg

        if not path.access(Path.R_OK):  # Проверка прав на чтение
            error_msg = f"Error: No read permissions - {path}"
            logger.warning(error_msg)
            return error_msg

        # Чтение файла
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            error_msg = f"Error: File is not UTF-8 encoded - {path}"
            logger.warning(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error while reading file: {str(e)}"
            logger.warning(error_msg)
            return error_msg
