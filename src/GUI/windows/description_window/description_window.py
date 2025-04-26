import os
import tkinter as tk
from tkinter import ttk

from markdown import markdown
from tkhtmlview import HTMLLabel

from src.GUI.styles import Styles
from src.logger.logger import setup_logger

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

        # Load the application description content
        description_file = "data/description_app.md"
        description = self._read_description_file(description_file)

        # Convert Markdown content to HTML
        html_content = markdown(description)
        html_content = f"""<div style="font-size: 12px;">{html_content}</div>"""

        # Main frame containing the HTML content
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Render the description as HTML
        self.html_label = HTMLLabel(
            self.main_frame,
            html=html_content,
            background="white",
            width=50,
            height=20
        )
        self.html_label.grid(row=0, column=0, sticky="nsew")

        # Adding a vertical scrollbar tied to the HTML label
        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.html_label.yview
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
            button_frame,
            text="Закрыть",
            command=self.destroy,
            style="Accent.TButton"
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
        current_scroll = self.html_label.yview()[0]  # Get current vertical scroll position
        self.update()

        # After resizing, restore the scroll position
        self.after(10, lambda: self.html_label.yview_moveto(current_scroll))

    def _read_description_file(self, file_path):

        if not os.path.exists(file_path):
            logger.warning("Error: Description file not found")
        if not os.path.isfile(file_path):
            logger.warning("Error: The specified path is not a file")
        if not os.access(file_path, os.R_OK):
            logger.warning("Error: Unable to read the description file")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Error while reading the file: {str(e)}"
