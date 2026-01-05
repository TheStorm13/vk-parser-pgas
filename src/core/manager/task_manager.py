from concurrent.futures import ThreadPoolExecutor
from threading import Event

from src.core.exception.task_interrupted_error import TaskInterruptedError
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class TaskManager:
    """Организует выполнение и остановку фоновой задачи.

    Args:
        root: Корневой UI-элемент.
        state_manager: Менеджер состояния.
        max_workers (int): Количество потоков.

    """

    def __init__(self, root, state_manager, max_workers=1):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.root = root
        self.state_manager = state_manager
        self.stop_event = Event()
        self.future = None

    def run_task(self, func, *args, **kwargs):
        """Запускает задачу, если другая не выполняется.

        Args:
            func (callable): Функция для запуска.
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Raises:
            RuntimeError: Задача уже выполняется.

        """
        if not self.stop_event.is_set():
            self.stop_event.clear()
            self.future = self.executor.submit(func, *args, **kwargs)
        else:
            raise RuntimeError("Task is running!")

    def stop_task(self):
        """Сигнализирует остановку текущей задачи."""
        self.stop_event.set()

    def raise_if_stopped(self):
        """Выбрасывает TaskInterruptedError при установленном флаге остановки.

        Raises:
            TaskInterruptedError: Задача остановлена пользователем.

        """
        if self.is_task_stopped():
            self.stop_event.clear()
            logger.info("The task was interrupted by the user")
            raise TaskInterruptedError("Задача была прервана пользователем!")

    def is_task_stopped(self) -> bool:
        """Проверяет флаг остановки задачи.

        Returns:
            bool: True при установленном флаге.

        """
        return self.stop_event.is_set()
