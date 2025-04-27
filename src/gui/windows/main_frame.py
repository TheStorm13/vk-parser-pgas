from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

from src.core.manager.state_manager import StateManager
from src.core.post_controller import PostController
from src.gui.component.button_component import ButtonComponent
from src.gui.component.form_component import FormComponent
from src.gui.component.logo_component import LogoComponent
from src.gui.component.progress_bar_component import ProgressBarComponent
from src.gui.manager.ui_state_manager import UIStateManager
from src.gui.windows.description_window import DescriptionWindow
from src.gui.windows.message_box import CustomMessageBox


class MainFrame:
    def __init__(self, root, state_manager):
        # todo: перенести от сюда

        # Single-thread executor for running background tasks
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None  # Holds the future result of background tasks

        self.state_manager = state_manager

        # Initialize the main components of the UI
        self.root = root
        self.style = self.root.style
        self.main_frame = ttk.Frame(self.root, padding=10, borderwidth=1, relief="sunken")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self._init_components()

        # Настройка колонок и строк для автоматического растяжения
        self.main_frame.columnconfigure(0, weight=1)
        for i in range(4):
            self.main_frame.rowconfigure(i, weight=0)

        # Manage UI controls' manager
        self.ui_state = UIStateManager([
            self.form_component.entry_vk_token,
            self.form_component.entry_vk_group,
            self.form_component.entry_start_date,
            self.form_component.entry_end_date,
            self.form_component.entry_full_name,
            self.buttons_component.button_run_stop,
            self.buttons_component.description_button

        ])

        # Initialize window geometry
        self.root.update_idletasks()
        self.root.geometry("")

    def _init_components(self):
        # Create and initialize
        self.form_component = FormComponent(self.main_frame, self.state_manager)
        self.form_component.frame.grid(row=0, column=0, sticky="new", pady=5)  # Форма идет первой

        self.progress_component = ProgressBarComponent(self.main_frame, self.state_manager)
        self.progress_component.frame.grid(row=1, column=0, pady=5)  # Прогресс-бар следует за формой

        self.buttons_component = ButtonComponent(self.main_frame,
                                                 self.run_program,
                                                 self.stop_program,
                                                 self.open_description_window)
        self.buttons_component.frame.grid(row=2, column=0, pady=5)

        self.logo_component = LogoComponent(self.main_frame, "data/logo.png")
        self.logo_component.frame.grid(row=3, column=0, sticky="ne", pady=5)  # Лого размещаем последним

    def run_program(self):
        # Start the main program logic as a background task
        try:
            # Prevent concurrent execution
            if self.future and not self.future.done():
                return

            # Validate and parse dates
            # todo: сделать валидацию данных
            # start_date, end_date = DateUtils.validate_dates(start_date, end_date)

            # Disable UI elements during processing
            self.form_component.enter_data()
            self.ui_state.disable_all()

            # Submit the program execution to the thread pool
            self.future = self.executor.submit(
                self._execute_program_logic,  # Logic to execute
                self.state_manager
            )

            # Add a callback to handle when the task is complete
            self.future.add_done_callback(self._on_task_complete)

        except Exception as e:
            self._handle_error(f"Ошибка при запуске: {str(e)}")
            self._reset_ui()

    def _on_task_complete(self, future):
        self.root.after(0, self._handle_task_completion, future)

    def _handle_task_completion(self, future):
        try:
            future.result()
        except InterruptedError:
            CustomMessageBox(self.root, "Информация", "Процесс остановлен")
        except Exception as e:
            self._handle_error(str(e))
        finally:
            self._reset_ui()

    def _execute_program_logic(self, state_manager: StateManager):
        # Core program logic for data processing
        try:
            # Show progress bar during processing
            self.root.after(0, self.progress_component.show)

            post_controller = PostController()

            post_controller.run(
                state_manager
            )

        except InterruptedError as e:
            self.root.after(0, CustomMessageBox, self.root, "Информация", "Процесс остановлен")
        except Exception as e:
            self.root.after(0, self._handle_error, str(e))
        finally:
            self.root.after(0, self._reset_ui)

    def _handle_error(self, error_message):
        # Show error message to the user
        CustomMessageBox(self.root, "Ошибка", error_message)
        self._reset_ui()

    def stop_program(self):
        # todo: добавить остановку программы
        # Stop the running program logic
        try:
            if self.future and not self.future.done():
                self.future.cancel()  # Attempt to cancel the task
                CustomMessageBox(
                    self.root,
                    "Информация",
                    "Процесс остановлен"
                )
        except Exception as e:
            self._handle_error(f"Ошибка при остановке: {str(e)}")
        finally:
            self._reset_ui()

    def _reset_ui(self):
        # Enable UI elements and hide the progress bar
        self.ui_state.enable_all()
        self.progress_component.hide()

    def _show_success_message(self, start_date, end_date, full_name):
        # todo: доработать сообщение об успехе
        CustomMessageBox(
            self.root,
            "Успешно",
            f"Программа успешно нашла посты для \n"
            f"{full_name}\n"
            f"с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}."
        )

    def open_description_window(self):
        # Open a new window with additional description
        description_window = DescriptionWindow(self.root)
        description_window.grab_set()
