from src.core.exception.task_interrupted_error import TaskInterruptedError
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.core.post_controller import PostController
from src.gui.windows.description_window import DescriptionWindow
from src.gui.windows.main.main_frame import MainFrame
from src.gui.windows.message_box import CustomMessageBox


class MainFrameController:
    """Управляет главным окном и жизненным циклом задач.

    Args:
        root: Корневой виджет Tkinter.
        state_manager: Состояние приложения.
        task_manager: Планировщик фоновых задач.

    """

    def __init__(self, root, state_manager: StateManager, task_manager: TaskManager):
        self.root = root
        self.state_manager = state_manager
        self.task_manager = task_manager

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
        """Запускает обработку в фоне и обновляет UI."""
        try:
            self.main_frame.form_component.enter_data()
            self.main_frame.ui_state.disable_all(
                exclude=[
                    self.main_frame.buttons_component.description_button,
                    self.main_frame.buttons_component.button_run_stop,
                ],
            )

            self.task_manager.run_task(
                self._execute_business_logic,
                state_manager=self.state_manager,
                task_manager=self.task_manager,
            )

        except Exception as e:
            self._message_window("Ошибка", f"Ошибка при запуске: \n{e!s}")

    def stop_program(self):
        """Останавливает фоновую задачу и сбрасывает UI."""
        try:
            if not self.task_manager.is_task_stopped():
                self.main_frame.ui_state.disable_all()
                self.task_manager.stop_task()
        except Exception as e:
            self._message_window("Ошибка", f"Ошибка при остановке: \n{e!s}")
        finally:
            self.main_frame.reset_ui()

    def _execute_business_logic(self, **kwargs):
        """Выполняет бизнес-логику и обрабатывает исключения.

        Args:
            **kwargs: Вспомогательные параметры вызова.

        Returns:
            None

        """
        try:
            # Гарантирует выполнение в потоке UI
            self.root.after(0, self.main_frame.progress_component.show)

            post_controller = PostController(self.state_manager, self.task_manager)
            post_controller.run()

        except TaskInterruptedError:
            self._message_window("Информация", "Процесс остановлен.")
        except Exception as e:
            self._message_window("Ошибка", f"Ошибка при запуске: {e!s}")
        else:
            self._message_window(
                "Успешно",
                f"Посты успешны проанализированы."
                f"Найдено: {self.state_manager.state.post_count}",
            )
        finally:
            self.main_frame.reset_ui()

    def _message_window(self, title, text):
        """Показывает модальное уведомление в главном окне.

        Args:
            title: Заголовок окна.
            text: Текст сообщения.

        Returns:
            None

        """
        # Планирует показ окна в главном потоке UI
        self.root.after(
            0,
            CustomMessageBox,
            self.root,
            title,
            text,
        )

    def open_description_window(self):
        """Открывает окно описания в модальном режиме."""
        description_window = DescriptionWindow(self.root)
        description_window.grab_set()  # Делает окно модальным
