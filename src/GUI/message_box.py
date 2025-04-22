import tkinter as tk
from tkinter import ttk


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="white")
        self.resizable(False, False)  # Запрещаем изменение размеров окна

        # Создание стилей
        self.style = ttk.Style()
        self.style.configure("Custom.TLabel", background="white", font=("Helvetica", 12))
        self.style.configure("Custom.TButton", font=("Helvetica", 12, "bold"), background="white")

        # Сообщение
        self.label_message = ttk.Label(self, text=message, style="Custom.TLabel", wraplength=350)
        self.label_message.pack(pady=20, padx=20)

        # Кнопка
        self.button_ok = ttk.Button(self, text=button_text, style="Custom.TButton", command=self.destroy)
        self.button_ok.pack(pady=10)

        # Автоматически подгоняем высоту окна под текст
        self.update_idletasks()  # Обновляем информацию о размерах виджетов
        self.adjust_window_height()
        self.center_window()

    def adjust_window_height(self):
        """
        Автоматически подгоняет высоту окна под содержимое.
        """
        # Получаем высоту текстового виджета
        text_height = self.label_message.winfo_reqheight()

        # Вычисляем необходимую высоту окна
        window_height = text_height + 100  # Добавляем отступы для кнопки и других элементов

        # Устанавливаем новую высоту окна
        self.geometry(f"400x{window_height}")

    def center_window(self):
        """
        Центрирует окно на экране.
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"+{x}+{y}")
