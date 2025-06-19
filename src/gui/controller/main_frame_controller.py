from src.core.exception.task_interrupted_error import TaskInterruptedError
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.core.post_controller import PostController
from src.gui.windows.description_window import DescriptionWindow
from src.gui.windows.main.main_frame import MainFrame
from src.gui.windows.message_box import CustomMessageBox


class MainFrameController:
    def __init__(self, root, state_manager: StateManager, task_manager: TaskManager):
        # Initialize the controller with application root, state manager, and task manager
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
                "open_description_window": self.open_description_window,
            },
        )

    def run_program(self):
        """
        Start the main program logic as a background task.
        This method also manages UI state for a running process.
        """
        try:
            # Disable UI elements to prevent further user actions during processing
            self.main_frame.form_component.enter_data()
            self.main_frame.ui_state.disable_all(
                exclude=[
                    self.main_frame.buttons_component.description_button,
                    self.main_frame.buttons_component.button_run_stop,
                ]
            )

            # Submit the main business logic to be executed in the background
            self.task_manager.run_task(
                self._execute_business_logic,
                state_manager=self.state_manager,
                task_manager=self.task_manager,
            )

        except Exception as e:
            # Notify the user of error
            self._message_window("Ошибка", f"Ошибка при запуске: \n{str(e)}")

    def stop_program(self):
        """
        Stop the currently running task.
        Disables the UI during stopping and ensures cleanup.
        """
        try:
            if not self.task_manager.is_task_stopped():
                # Disable all UI elements to ensure no actions are performed during stop
                self.main_frame.ui_state.disable_all()
                self.task_manager.stop_task()
        except Exception as e:
            # Notify the user of error
            self._message_window("Ошибка", f"Ошибка при остановке: \n{str(e)}")
        finally:
            # Reset UI to its default state after stopping
            self.main_frame.reset_ui()

    def _execute_business_logic(self, **kwargs):
        """
        Internal method to execute business logic.
        Handles interaction with the PostController and manages potential exceptions.
        """
        try:
            # Show progress indicator
            self.root.after(0, self.main_frame.progress_component.show)

            # Initialize PostController and run main logic
            post_controller = PostController(self.state_manager, self.task_manager)
            post_controller.run()

        except TaskInterruptedError:
            # Handle task interruption gracefully
            self._message_window("Информация", "Процесс остановлен.")
        except Exception as e:
            # Notify the user of error
            self._message_window("Ошибка", f"Ошибка при запуске: {str(e)}")
        else:
            # Notify the user of successful task completion
            self._message_window(
                "Успешно",
                f"Посты успешны проанализированы."
                f"Найдено: {self.state_manager.state.post_count}",
            )
        finally:
            # Reset UI after task execution (either success or failure)
            self.main_frame.reset_ui()

    def _message_window(self, title, text):
        """
        Helper method to display a message box on the UI.
        Used for error, success, or informational notifications.
        """
        self.root.after(
            0,  # Execute UI changes immediately after the current callback
            CustomMessageBox,  # The custom message box class or function
            self.root,
            title,
            text,
        )

    def open_description_window(self):
        """
        Open a new window to show additional descriptions or details to the user.
        """
        description_window = DescriptionWindow(self.root)
        description_window.grab_set()  # Ensure the new window is modal (blocks interaction with the main window)
