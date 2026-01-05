import tkinter as tk
from tkinter import ttk


class CustomMessageBox(tk.Toplevel):
    """Показывает модальное окно сообщения."""

    def __init__(self, parent, title, message, button_text="OK"):
        """Инициализирует окно, стили и элементы.

        Args:
            parent: Родительское окно Tk.
            title: Заголовок окна (str).
            message: Текст сообщения (str).
            button_text: Текст кнопки (str).

        Returns:
            None

        """
        super().__init__(parent)
        self.title(title)
        self.configure(bg="white")
        self.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure(
            "Custom.TLabel", background="white", font=("Helvetica", 12),
        )
        self.style.configure(
            "Custom.TButton", font=("Helvetica", 12, "bold"), background="white",
        )

        self.label_message = ttk.Label(
            self, text=message, style="Custom.TLabel", wraplength=580,
        )
        self.label_message.pack(pady=20, padx=20)

        self.button_ok = ttk.Button(
            self, text=button_text, style="Custom.TButton", command=self.destroy,
        )
        self.button_ok.pack(pady=10)

        self.update_idletasks()
        self.adjust_window_height()

    def adjust_window_height(self):
        """Подгоняет высоту окна под высоту текста.

        Returns:
            None

        """
        text_height = self.label_message.winfo_reqheight()
        window_height = text_height + 200
        self.geometry(f"600x{window_height}")
