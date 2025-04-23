from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

from src.GUI.manager.ui_state_manager import UIStateManager
from src.GUI.windows.description_window.description_window import DescriptionWindow
from src.GUI.windows.main_window.form_component import FormComponent
from src.GUI.windows.main_window.logo_component import LogoComponent
from src.GUI.windows.main_window.progress_bar_manager import ProgressBarManager
from src.GUI.windows.message_window.message_box import CustomMessageBox
from src.logic.logic import MainLogic
from src.utils.intup_validator import InputValidator


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.main_frame = root.main_frame
        self.label_font = root.label_font

        self.form = FormComponent(self.main_frame, self.label_font)
        self.progress_manager = ProgressBarManager(self.main_frame, self.label_font)
        self.validator = InputValidator()

        self.executor = ThreadPoolExecutor(max_workers=1)  # Пул для задач
        self.future = None  # Для отслеживания текущей задачи

        # Подключение логотипа
        self.logo_component = LogoComponent(self.main_frame, "data/logo.png")

        self._create_buttons()

        self.ui_state = UIStateManager([
            self.form.entry_start_date,
            self.form.entry_end_date,
            self.form.entry_full_name,
            self.button_run_stop,
            self.description_button

        ])

        # Настройка авторазмера окна
        self.root.update_idletasks()
        self.root.geometry("")

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
        self.button_run_stop = ttk.Button(
            self.main_frame,
            text="Запустить",
            command=self.run_program,
            style="Accent.TButton",
            takefocus=False
        )
        self.button_run_stop.grid(row=7, column=0, columnspan=2, pady=10)

        # Добавление кнопки для вызова окна описания
        self.description_button = ttk.Button(
            self.main_frame,
            text="Описание",
            command=self.open_description_window,  # Привязываем метод открытия окна
            style="Accent.TButton"
        )
        self.description_button.grid(row=8, column=0, columnspan=2, pady=10)

    def toggle_run_stop(self):
        """Переключатель для кнопки между состояниями 'Запустить' и 'Остановить'"""
        if self.button_run_stop["text"] == "Запустить":
            # Запускаем процесс если валидация прошла успешно
            self.button_run_stop.config(text="Остановить", style="Danger.TButton")
            self.run_program()
        else:
            self.button_run_stop.config(text="Запустить", style="Accent.TButton")
            self.stop_program()

    def run_program(self):
        """Обработчик нажатия на кнопку 'Запустить', запускает длительную операцию"""
        try:
            # Проверяем, не запущена ли уже задача
            if self.future and not self.future.done():
                return

            # Получение и валидация данных из формы
            start_date = self.form.entry_start_date.get()
            end_date = self.form.entry_end_date.get()
            full_name = self.form.entry_full_name.get()

            # start_date = "01.09.2024"
            # end_date = "01.10.2024"
            # full_name = "Гроза Илья Валерьевич"

            start_date, end_date = self.validator.validate_dates(start_date, end_date)

            # Отключение UI и подготовка к выполнению
            self.ui_state.disable_all()

            # Запуск в отдельном потоке
            self.future = self.executor.submit(
                self._execute_program_logic,  # Функция, которая будет выполняться
                start_date, end_date, full_name  # Аргументы для функции
            )

            self.future.add_done_callback(self._on_task_complete)

        except Exception as e:
            print(f"Ошибка при запуске: {str(e)}")
            self._handle_error(f"Ошибка при запуске: {str(e)}")
            self._reset_ui()

    def _on_task_complete(self, future):
        """Обработчик завершения задачи"""
        self.root.after(0, self._handle_task_completion, future)

    def _handle_task_completion(self, future):
        """Обрабатывает результат задачи из главного потока"""
        try:
            future.result()  # Проверяем на наличие исключений
        except InterruptedError:
            CustomMessageBox(self.root, "Информация", "Процесс остановлен")
        except Exception as e:
            self._handle_error(str(e))
        finally:
            self._reset_ui()

    def _execute_program_logic(self, start_date, end_date, full_name):
        try:
            # Показываем прогресс бар в основном потоке
            self.root.after(0, self.progress_manager.show)

            # Инициализация основной логики
            main_logic = MainLogic()

            # Выполнение основной логики с проверкой остановки
            main_logic.run(
                full_name,
                start_date,
                end_date,
                self._update_progress
            )

        except InterruptedError as e:
            self.root.after(0, CustomMessageBox, self.root, "Информация", "Процесс остановлен")
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))
        finally:
            self.root.after(0, self._reset_ui)

    def _handle_error(self, error_message):
        """Обработка ошибок с отображением сообщения"""
        CustomMessageBox(self.root, "Ошибка", error_message)
        self._reset_ui()

    def stop_program(self):
        """Обработчик нажатия на кнопку 'Остановить', корректно завершает задачу"""
        # todo: добавить остановку программы
        try:
            if self.future and not self.future.done():
                self.future.cancel()
                CustomMessageBox(
                    self.root,
                    "Информация",
                    "Процесс остановлен"
                )
        except Exception as e:
            self._handle_error(f"Ошибка при остановке: {str(e)}")
        finally:
            self._reset_ui()

    def _validate_input(self):

        return True

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
