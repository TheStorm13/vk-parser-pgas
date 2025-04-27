from concurrent.futures import ThreadPoolExecutor
from threading import Event

from src.core.exception.task_interrupted_exception import TaskInterruptedException
from src.infrastructure.logger.logger import setup_logger

logger=setup_logger(__name__)

class TaskManager:
    def __init__(self, root, state_manager, max_workers=2):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.root = root
        self.state_manager = state_manager
        self.stop_event = Event()
        self.future = None

    def run_task(self, func, callback=None, *args, **kwargs):
        if not self.stop_event.is_set():
            self.stop_event.clear()
            self.future = self.executor.submit(func, *args, **kwargs)
            if callback:
                self.future.add_done_callback(
                    lambda f: self.root.after(0, callback, f)
                )
        else:
            raise RuntimeError("Task is running!")

    def stop_task(self):
        self.stop_event.set()

    def raise_if_stopped(self):
        """Выбрасывает исключение, если установлен флаг остановки."""
        if self.is_task_stopped():
            self.stop_event.clear()
            logger.info("Task was interrupted")
            raise TaskInterruptedException("Task was interrupted")


    def is_task_stopped(self):
        return self.stop_event.is_set()
