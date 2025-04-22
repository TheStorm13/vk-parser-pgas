import threading
from datetime import datetime
from tkinter import font as tkfont
from tkinter import ttk

from ttkthemes import ThemedTk

from src.logic.logic import MainLogic
from .message_box import CustomMessageBox


class ModernApp(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("Сбор постов для ПГАС")
        self.geometry("600x680")
        self.center_window()
        self.set_theme("arc")  # Используем современную тему

        # Убираем лишние отступы и границы
        self.configure(bg="white")  # Устанавливаем фон окна
        self.main_frame = ttk.Frame(self, padding=10)  # Убираем лишний паддинг
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)  # Убираем лишние отступы

        # Настройка стилей
        self.style = ttk.Style()
        self.style.configure("TFrame", background="white", borderwidth=0)  # Убираем границы у Frame
        self.style.configure("TLabel", background="white", font=("Helvetica", 12))  # Настраиваем стиль для Label
        self.style.configure("TButton", font=("Helvetica", 12, "bold"))  # Настраиваем стиль для Button

        # Отключаем фокусный индикатор для кнопки
        self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = tkfont.Font(family="Helvetica", size=12)
        self.button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Сбор постов для ПГАС", font=self.title_font)
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Start Date
        self.label_start_date = ttk.Label(self.main_frame, text="Начальная дата (дд.мм.гггг):", font=self.label_font)
        self.label_start_date.grid(row=1, column=0, sticky="w", pady=5)
        self.entry_start_date = ttk.Entry(self.main_frame, font=self.label_font)
        self.entry_start_date.grid(row=1, column=1, sticky="ew", pady=5)

        # End Date
        self.label_end_date = ttk.Label(self.main_frame, text="Конечная дата (дд.мм.гггг):", font=self.label_font)
        self.label_end_date.grid(row=2, column=0, sticky="w", pady=5)
        self.entry_end_date = ttk.Entry(self.main_frame, font=self.label_font)
        self.entry_end_date.grid(row=2, column=1, sticky="ew", pady=5)

        # Full Name
        self.label_full_name = ttk.Label(self.main_frame, text="ФИО:", font=self.label_font)
        self.label_full_name.grid(row=3, column=0, sticky="w", pady=5)
        self.entry_full_name = ttk.Entry(self.main_frame, font=self.label_font)
        self.entry_full_name.grid(row=3, column=1, sticky="ew", pady=5)

        # Run Button
        self.button_run = ttk.Button(
            self.main_frame,
            text="Запустить",
            command=self.run_program,
            style="Accent.TButton",
            takefocus=False  # Отключаем возможность фокусировки на кнопке
        )
        self.button_run.grid(row=4, column=0, columnspan=2, pady=20)

        # Configure grid weights for resizing
        self.main_frame.columnconfigure(1, weight=1)

        # Добавляем поддержку копирования и вставки
        self.bind_copy_paste_events()

        # Добавляем прогресс-бар
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        self.progress_label = ttk.Label(self.main_frame, text="0", font=self.label_font)
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=5)
        self.progress.grid_remove()  # Скрываем прогресс-бар при запуске
        self.progress_label.grid_remove()  # Скрываем progress_label при запуске

        # Описание внизу окна
        self.description_label = ttk.Label(
            self.main_frame,
            text="""
Данное приложение предназначено для сбора постов из группы ВКонтакте за указанный период времени для ПГАС. 
Чтобы начать работу, укажите начальную и конечную даты сбора постов, введите ФИО и нажмите кнопку «Запустить». 
 
Программа будет искать все возможные комбинации и сокращения ваших ФИО в тексте постов и комментариях. Обязательно указывайте для определения авторства "Текст: ...". Пример подписи: "Текст: Гроза Илья".
                    
После завершения работы программы в папке с приложением будут созданы два текстовых файла:  
                    
1. posts.txt  
В этом файле содержится информация о категориях и список всех постов.  
                    
2. for_word_file.md
Этот файл содержит информацию для удобного копирования в таблицу Word. 
Просто скопируйте данные для каждой категории в соответствующий столбец.  
                    
Рекомендуется проверить посты через ссылки.
                    """,
            wraplength=550,  # Автоматический перенос текста
            justify="center",  # Выравнивание текста по центру
            font=("Helvetica", 10)  # Шрифт и размер текста
        )
        self.description_label.grid(row=7, column=0, columnspan=2, pady=20)

        self.main_frame.columnconfigure(1, weight=1)

    def bind_copy_paste_events(self):
        # Привязываем горячие клавиши для копирования и вставки
        self.bind_all("<Control-KeyRelease>", self.handle_keypress)  # Обработка всех Ctrl+клавиш

    def handle_keypress(self, event):
        # Обработка физических клавиш
        if event.keycode == 67:  # Код клавиши C (Ctrl+C)
            self.copy_text()
        elif event.keycode == 86:  # Код клавиши V (Ctrl+V)
            self.paste_text()
        elif event.keycode == 88:  # Код клавиши X (Ctrl+X)
            self.cut_text()

    def copy_text(self, event=None):
        # Копирование текста
        widget = self.focus_get()  # Получаем текущий активный виджет
        if isinstance(widget, ttk.Entry):  # Используем ttk.Entry
            widget.event_generate("<<Copy>>")
            widget.select_clear()

    def paste_text(self, event=None):
        # Вставка текста
        widget = self.focus_get()  # Получаем текущий активный виджет
        if isinstance(widget, ttk.Entry):  # Используем ttk.Entry
            widget.event_generate("<<Paste>>")
            widget.select_clear()

    def cut_text(self, event=None):
        # Вырезание текста
        widget = self.focus_get()  # Получаем текущий активный виджет
        if isinstance(widget, ttk.Entry):  # Используем ttk.Entry
            widget.event_generate("<<Cut>>")
            widget.select_clear()

    def update_progress(self, progress, total_progress):
        self.progress['value'] = (progress / total_progress) * 100
        self.progress_label.config(text=f"{int(progress)}")
        self.update_idletasks()

    def run_program(self):
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        full_name = self.entry_full_name.get()

        # start_date = "01.09.2024"
        # end_date = "01.10.2024"
        # full_name = "Гроза Илья Валерьевич"

        # Проверяем формат даты
        try:
            start_date = datetime.strptime(start_date, "%d.%m.%Y")
            end_date = datetime.strptime(end_date, "%d.%m.%Y")
        except ValueError:
            CustomMessageBox(self, "Ошибка", "Не тот формат. Используйте дд.мм.гггг.")
            return

        # Меняем кнопку на "Process" и делаем её неактивной
        self.button_run.config(text="Выполняется...", state="disabled")

        # Убираем фокус с кнопки
        self.button_run.master.focus_set()

        # Запускаем длительную операцию в отдельном потоке
        threading.Thread(
            target=self._execute_program_logic,  # Метод, который будет выполняться в потоке
            args=(start_date, end_date, full_name),  # Аргументы для метода
            daemon=True  # Поток завершится, если завершится основная программа
        ).start()

    def _execute_program_logic(self, start_date, end_date, full_name):
        # Показываем прогресс-бар
        self.progress.grid()
        self.progress_label.grid()

        # Выполнение длительной операции
        main_logic = MainLogic()
        main_logic.run(full_name, start_date, end_date, self.update_progress)

        # Возвращаем кнопку в исходное состояние после завершения
        self.after(0, self._reset_button)

        # Показываем сообщение об успешном завершении
        self.after(0, self._show_success_message, start_date, end_date, full_name)

        self.progress.grid_remove()
        self.progress_label.grid_remove()  # Скрываем progress_label при запуске
        self.progress['value'] = 0
        self.progress_label.config(text=f"{int(0)}")

    def _reset_button(self):
        # Возвращаем кнопку в исходное состояние
        self.button_run.config(text="Запустить", state="normal")

    def _show_success_message(self, start_date, end_date, full_name):
        # Показываем сообщение об успешном завершении
        CustomMessageBox(self,
                         "Успешно",
                         f"Программа успешно нашла посты для {full_name} с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}."
                         )

    def center_window(self):
        """
        Центрирует окно на экране.
        """
        self.update_idletasks()  # Обновляем информацию о размерах окна
        width = self.winfo_width()  # Ширина окна
        height = self.winfo_height()  # Высота окна
        screen_width = self.winfo_screenwidth()  # Ширина экрана
        screen_height = self.winfo_screenheight()  # Высота экрана

        # Вычисляем координаты для центрирования окна
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Устанавливаем положение окна
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()
