from ttkthemes import ThemedTk

from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.gui.controller.main_frame_controller import MainFrameController
from src.gui.styles import Styles
from src.gui.windows.message_box import CustomMessageBox
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class MainApplication(ThemedTk):
    """Запускает главное окно приложения."""

    def __init__(self):
        """Инициализирует окно, менеджеры и контроллеры.

        Returns:
            None

        """
        super().__init__()
        self.state_manager = StateManager()
        self.task_manager = TaskManager(self, self.state_manager)

        self.title("Сбор постов для ПГАС")
        self.geometry("800x800")
        self.set_theme("arc")

        self.style = Styles.configure_styles(self)
        self.configure(bg="white")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.main_frame = MainFrameController(
            self, self.state_manager, self.task_manager,
        )

        self.style.map("Accent.TButton", focus=[("focus", "!focus", "")])

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Завершает приложение и останавливает задачи.

        Returns:
            None

        """
        try:
            if self.task_manager.is_task_stopped():
                self.task_manager.stop_task()
                CustomMessageBox(self, "Информация", "Все фоновые задачи остановлены.")
        except Exception as e:
            logger.error(f"Ошибка при завершении программы: {e!s}")
        finally:
            self.destroy()
