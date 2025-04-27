from src.core.exception.task_interrupted_exception import TaskInterruptedException
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.core.model.state_app import StateApp
from src.core.post_controller import PostController
from src.gui.windows.main_frame import MainFrame
from src.gui.windows.message_box import CustomMessageBox


class MainFrameController:
    def __init__(self, root, state_manager:StateManager, task_manager:TaskManager):
        self.root = root
        self.state_manager = state_manager
        self.task_manager = task_manager

        # Initialize MainFrame and pass callbacks
        self.main_frame = MainFrame(
            self.root,
            self.state_manager,
            button_callbacks={
                "run_program": self.run_program,
                "stop_program": self.stop_program,
            },
        )

    def run_program(self):
        # Start the main program logic as a background task
        try:
            # Validate and parse dates
            # todo: сделать валидацию данных
            # start_date, end_date = DateUtils.validate_dates(start_date, end_date)

            # Disable UI elements during processing
            self.main_frame.form_component.enter_data()
            self.main_frame.ui_state.disable_all(exclude=[
                self.main_frame.buttons_component.description_button,
                self.main_frame.buttons_component.button_run_stop
            ])

            # Submit the program execution to the thread pool
            self.task_manager.run_task(
                self._execute_business_logic,
                callback=self._handle_task_completion,
                state_manager=self.state_manager,
                task_manager=self.task_manager
            )

        except Exception as e:
            self._handle_error(f"Ошибка при запуске: {str(e)}")

    def stop_program(self):
        try:
            if not self.task_manager.is_task_stopped():
                self.main_frame.ui_state.disable_all()
                self.task_manager.stop_task()
        except Exception as e:
            self._handle_error(f"Ошибка при остановке: {str(e)}")

    def _execute_business_logic(self, **kwargs):
        try:
            self.root.after(0, self.main_frame.progress_component.show)
            post_controller = PostController(self.state_manager, self.task_manager)
            post_controller.run()
        except TaskInterruptedException:
            self.root.after(0, CustomMessageBox, self.root, "Информация", "Процесс остановлен.")
        except Exception as e:
            raise e
        finally:
            self.root.after(0, self.main_frame.reset_ui)

    def _handle_task_completion(self, future):
        CustomMessageBox(self.root,
                         "Успешно",
                         f"Посты успешны проанализированы."
                         f"Найдено: {self.state_manager.state.post_count}"
                         )

    def _handle_error(self, error_message):
        """Show an error."""
        CustomMessageBox(self.root, "Ошибка", error_message)
