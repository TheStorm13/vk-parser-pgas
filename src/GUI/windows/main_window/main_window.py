import threading
from tkinter import ttk

from src.GUI.intup_validator import InputValidator
from src.GUI.ui_state_manager import UIStateManager
from src.GUI.windows.main_window.description_window.description_window import DescriptionWindow
from src.GUI.windows.main_window.form_component import FormComponent
from src.GUI.windows.main_window.progress_bar_manager import ProgressBarManager
from src.GUI.windows.message_box import CustomMessageBox
from src.logic.logic import MainLogic


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.main_frame = root.main_frame
        self.label_font = root.label_font

        self.form = FormComponent(self.main_frame, self.label_font)
        self.progress_manager = ProgressBarManager(self.main_frame, self.label_font)
        self.validator = InputValidator()
        self.ui_state = UIStateManager([
            self.form.entry_start_date,
            self.form.entry_end_date,
            self.form.entry_full_name
        ])

        self._create_buttons()

    def create_label(self):
        """Создает заголовок окна"""
        self.title_label = ttk.Label(
            self.main_frame,
            text="Сбор постов для ПГАС",
            font=self.label_font
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def _create_buttons(self):
        """Создает кнопки интерфейса"""
        self.button_run = ttk.Button(
            self.main_frame,
            text="Запустить",
            command=self.run_program,
            style="Accent.TButton",
            takefocus=False
        )
        self.button_run.grid(row=7, column=0, columnspan=2, pady=10)

        # Добавление кнопки для вызова окна описания
        self.description_button = ttk.Button(
            self.main_frame,
            text="Описание",
            command=self.open_description_window,  # Привязываем метод открытия окна
            style="Accent.TButton"
        )
        self.description_button.grid(row=8, column=0, columnspan=2, pady=10)

    def run_program(self):
        """Обработчик нажатия на кнопку 'Запустить', запускает длительную операцию"""
        # Validate input
        # if not self._validate_input():
        #     return

        # Disable the UI and start the processing
        # todo: отключить интерфейс при работе
        self.ui_state.disable_all()
        self._start_processing()

    def _validate_input(self):
        # todo
        return True

    def _start_processing(self):
        start_date = self.form.entry_start_date.get()
        end_date = self.form.entry_end_date.get()
        full_name = self.form.entry_full_name.get()

        start_date = "01.09.2024"
        end_date = "01.10.2024"
        full_name = "Гроза Илья Валерьевич"

        start_date, end_date = self.validator.validate_dates(start_date, end_date)

        # Запускаем длительную операцию в отдельном потоке
        threading.Thread(
            target=self._execute_program_logic,  # Метод, который будет выполняться в потоке
            args=(start_date, end_date, full_name),  # Аргументы для метода
            daemon=True  # Поток завершится, если завершится основная программа
        ).start()

    def _execute_program_logic(self, start_date, end_date, full_name):
        try:
            # Show progress bar
            self.progress_manager.show()

            # Выполнение длительной операции
            main_logic = MainLogic()
            main_logic.run(full_name, start_date, end_date, self._update_progress)

            # Show success message
            self.root.after(0, self._show_success_message, start_date, end_date, full_name)


        except Exception as e:
            CustomMessageBox(self.root, "Ошибка", f"Возникла ошибка: {str(e)}")

        finally:
            # Reset UI state and progress bar
            # todo: включить интерфейс после работы
            self.root.after(0, self._reset_ui)

    def _update_progress(self, progress, total_progress):
        """Обновляет прогресс на прогресс-баре"""
        self.progress_manager.update(progress, total_progress)

    def _reset_ui(self):
        """Сбрасывает UI к исходному состоянию"""
        self.ui_state.enable_all()
        self.progress_manager.hide()

    def _show_success_message(self, start_date, end_date, full_name):
        """Показывает сообщение об успешном завершении операции"""
        # todo: доработать сообщение об успехе
        CustomMessageBox(
            self.root,
            "Успешно",
            f"Программа успешно нашла посты для {full_name} с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}."
        )

    def open_description_window(self):
        """
        Открытие окна описания.
        """
        description_window = DescriptionWindow(self.root)  # Создаем экземпляр окна описания
        description_window.grab_set()  # Блокируем главное окно, пока не закроется новое
