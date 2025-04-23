import os
import tkinter as tk
from tkinter import ttk


class DescriptionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Описание")
        self.configure(bg="white")
        # todo: текст должен всегда помещаться вертикльно
        self.geometry("900x700")
        self.minsize(600, 400)
        self.resizable(True, True)  # Запрещаем изменение размеров окна

        # Подгоняем стиль
        self.style = ttk.Style()
        self.style.configure("Custom.TLabel", background="white", font=("Helvetica", 12), justify="left",
                             wraplength=550)

        # Чтение описания из файла с дополнительными проверками
        description_file = "description_app.txt"
        description = self._read_description_file(description_file)

        # Создаем рамку для текста и прокрутки
        frame = ttk.Frame(self)
        frame.pack(pady=10, padx=10, expand=True, fill="both")

        # Создаем виджет Text для отображения текста
        self.text_description = tk.Text(frame, wrap="word", font=("Helvetica", 12),
                                        bg="white", relief="flat", state="normal")
        self.text_description.insert("1.0", description)
        self.text_description.configure(state="disabled")  # Запрещаем редактирование текста
        self.text_description.pack(side="left", expand=True, fill="both")

        # Создаем вертикальный скроллбар
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_description.yview)
        scrollbar.pack(side="right", fill="y")

        # Привязываем виджет текста к скроллбару
        self.text_description.configure(yscrollcommand=scrollbar.set)

        # todo: кнопка должна быть всегда видна

        # Создаем нижнюю рамку для кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=10)  # Размещаем ее внизу

        # Добавляем кнопку закрытия
        close_button = ttk.Button(button_frame, text="Закрыть", command=self.destroy)
        close_button.pack(pady=5)

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
