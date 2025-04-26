from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

from src.GUI.manager.ui_state_manager import UIStateManager
from src.GUI.windows.description_window.description_window import DescriptionWindow
from src.GUI.windows.main_window.form_component import FormComponent
from src.GUI.windows.main_window.logo_component import LogoComponent
from src.GUI.windows.main_window.progress_bar_manager import ProgressBarManager
from src.GUI.windows.message_window.message_box import CustomMessageBox
from src.logic.post_controller import PostController
from src.state.state_app import StateApp
from src.state.state_storage import StateStorage
from src.utils.data_utils import DateUtils


class MainWindow:
    def __init__(self, root, state):
        #todo: перенести от сюда

        # Single-thread executor for running background tasks
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None  # Holds the future result of background tasks
        self.state = state
        self.state_storage= StateStorage(state)

        # Initialize the main components of the UI
        self.root = root
        self.main_frame = root.main_frame
        self.label_font = root.label_font

        # Create and initialize
        self.form = FormComponent(self.main_frame, self.label_font,self.state)
        self.progress_manager = ProgressBarManager(self.main_frame, self.label_font)
        self.logo_component = LogoComponent(self.main_frame, "data/logo.png")
        self._create_buttons()



        # Manage UI controls' state
        self.ui_state = UIStateManager([
            self.form.entry_vk_token,
            self.form.entry_vk_group,
            self.form.entry_start_date,
            self.form.entry_end_date,
            self.form.entry_full_name,
            self.button_run_stop,
            self.description_button

        ])

        # Initialize window geometry
        self.root.update_idletasks()
        self.root.geometry("")

    def create_label(self):
        self.title_label = ttk.Label(
            self.main_frame,
            text="Сбор постов для ПГАС",
            font=self.label_font
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    def _create_buttons(self):
        self.button_run_stop = ttk.Button(
            self.main_frame,
            text="Запустить",
            command=self.run_program,
            style="Accent.TButton",
            takefocus=False
        )
        self.button_run_stop.grid(row=9, column=0, columnspan=2, pady=10)

        self.description_button = ttk.Button(
            self.main_frame,
            text="Описание",
            command=self.open_description_window,
            style="Accent.TButton"
        )
        self.description_button.grid(row=10, column=0, columnspan=2, pady=10)

    def toggle_run_stop(self):
        # Toggle the button between "Run" and "Stop"
        if self.button_run_stop["text"] == "Запустить":
            self.button_run_stop.config(text="Остановить", style="Danger.TButton")
            self.run_program()
        else:
            self.button_run_stop.config(text="Запустить", style="Accent.TButton")
            self.stop_program()

    def run_program(self):
        # Start the main program logic as a background task
        try:
            # Prevent concurrent execution
            if self.future and not self.future.done():
                return

            # Get user inputs
            vk_token = self.form.entry_vk_token.get()
            vk_group_name = self.form.entry_vk_group.get()
            start_date = self.form.entry_start_date.get()
            end_date = self.form.entry_end_date.get()
            full_name = self.form.entry_full_name.get()

            # Validate and parse dates
            start_date, end_date = DateUtils.validate_dates(start_date, end_date)

            self.state = StateApp(
                vk_token=vk_token,
                vk_group_url=vk_group_name,
                full_name=full_name,
                start_date=start_date,
                end_date=end_date
            )

            # Disable UI elements during processing
            self.ui_state.disable_all()

            # Submit the program execution to the thread pool
            self.future = self.executor.submit(
                self._execute_program_logic,  # Logic to execute
                self.state
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
            self.state_storage.save_state()

    def _execute_program_logic(self, state: StateApp):
        # Core program logic for data processing
        try:
            # Show progress bar during processing
            self.root.after(0, self.progress_manager.show)

            post_controller = PostController()

            post_controller.run(
                state,
                self._update_progress
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

    def _update_progress(self, progress, total_progress):
        # Update the progress bar
        self.progress_manager.update(progress, total_progress)

    def _reset_ui(self):
        # Enable UI elements and hide the progress bar
        self.ui_state.enable_all()
        self.progress_manager.hide()

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
