from concurrent.futures import ThreadPoolExecutor
from threading import Event

from src.core.exception.task_interrupted_error import TaskInterruptedError
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class TaskManager:
    def __init__(self, root, state_manager, max_workers=1):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.root = root
        self.state_manager = state_manager
        self.stop_event = Event()  # Event used for signaling task termination
        self.future = None  # Placeholder for storing future objects

    def run_task(self, func, *args, **kwargs):
        """
        Submit a task to the ThreadPoolExecutor if no task is currently running.

        Args:
            func (callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Raises:
            RuntimeError: If a task is already running.
        """

        if not self.stop_event.is_set():
            self.stop_event.clear()  # Ensure the stop_event is reset
            self.future = self.executor.submit(
                func, *args, **kwargs
            )  # Submit task to the executor
        else:
            raise RuntimeError(
                "Task is running!"
            )  # Prevent multiple tasks from running concurrently

    def stop_task(self):
        """
        Signal the currently running task to stop by setting the stop_event.
        """
        self.stop_event.set()

    def raise_if_stopped(self):
        """
        Raise TaskInterruptedError if the stop_event is set.
        Clears the stop flag and logs an interruption message.

        Raises:
            TaskInterruptedError: If the task has been stopped.
        """
        if self.is_task_stopped():
            self.stop_event.clear()  # Reset the stop flag for future tasks
            logger.info("The task was interrupted by the user")  # Log the interruption
            raise TaskInterruptedError(
                "Задача была прервана пользователем!"
            )  # Notify that the task was stopped

    def is_task_stopped(self):
        """
        Check if the stop_event is set, indicating the task should stop.

        Returns:
            bool: True if the task is signaled to stop, False otherwise.
        """
        return self.stop_event.is_set()
