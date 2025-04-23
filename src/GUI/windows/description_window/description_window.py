import os
import tkinter as tk
from tkinter import ttk

from markdown import markdown
from tkhtmlview import HTMLLabel

from src.GUI.styles import Styles


class DescriptionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Описание")
        self.configure(bg="white")
        self.resizable(True, False)  # Запрещаем изменение размеров окна
        self.geometry("600x600")
        self.minsize(100, 100)
        self.maxsize(800, 800)

        # Подгоняем стиль
        self.style = Styles.configure_styles(self)

        # Чтение описания из файла с дополнительными проверками
        description_file = "data/description_app.md"
        description = self._read_description_file(description_file)

        # Конвертируем Markdown в HTML
        html_content = markdown(description)

        # Добавляем CSS для управления размером шрифта
        html_content = f"""<div style="font-size: 12px;">{html_content}</div>"""

        # Создаем фрейм для контента
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # HTML Label с собственным скроллбаром
        self.html_label = HTMLLabel(
            self.main_frame,
            html=html_content,
            background="white",
            width=50,  # Установите подходящую ширину
            height=20  # Установите подходящую высоту
        )
        self.html_label.grid(row=0, column=0, sticky="nsew")

        # Скроллбар
        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.html_label.yview  # Привязываем напрямую к html_label
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Привязываем скроллбар к html_label
        self.html_label.configure(yscrollcommand=self.scrollbar.set)

        # Нижний фрейм для кнопки
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, pady=(10, 10), sticky="ew")
        button_frame.columnconfigure(0, weight=1)

        close_button = ttk.Button(
            button_frame,
            text="Закрыть",
            command=self.destroy,
            style="Accent.TButton"
        )
        close_button.grid(row=0, column=0)

        # Настройка весов для растяжения
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """
        Обработчик события изменения размера окна.
        """
        # Сохраняем текущую позицию скроллбара до обновления
        current_scroll = self.html_label.yview()[0]

        # Даем время для перерисовки виджетов
        self.update()

        # Устанавливаем позицию скролла после короткой задержки
        self.after(10, lambda: self.html_label.yview_moveto(current_scroll))

    def _read_description_file(self, file_path):
        """
        Проверяет существование и доступность файла, а затем считывает его содержимое.
        """
        if not os.path.exists(file_path):
            print("Ошибка: Файл описания не найден.")
        if not os.path.isfile(file_path):
            print("Ошибка: Указанный путь не является файлом.")
        if not os.access(file_path, os.R_OK):
            print("Ошибка: Файл описания недоступен для чтения.")

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            return f"Ошибка при чтении файла: {str(e)}"
