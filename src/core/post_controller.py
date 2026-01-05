import time

from src.core.api_handlers.vk_api_handler import VKAPIHandler
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.core.post_processing.post_analyzer import PostAnalyzer
from src.core.report.report_creator import ReportCreator
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class PostController:
    """Управляет получением, анализом и отчетами по постам."""

    def __init__(self, state_manager: StateManager, task_manager: TaskManager):
        """Инициализирует контроллер постов.

        Args:
            state_manager: Менеджер состояния приложения.
            task_manager: Менеджер фоновых задач.

        """
        self.state_manager = state_manager
        self.task_manager = task_manager

    def run(self):
        """Запускает процесс: получает посты, анализирует и создает отчеты.

        Returns:
            None

        Raises:
            TaskInterruptedError: При остановке задачи.

        """
        vk_handler = VKAPIHandler(
            self.state_manager, self.task_manager,
        )
        post_analyzer = PostAnalyzer(
            self.state_manager,
        )
        report_creator = ReportCreator(
            self.state_manager,
        )

        start_time = time.time()
        posts = vk_handler.get_posts()
        logger.info(f"Time to fetch posts: {(time.time() - start_time)}")

        self.task_manager.raise_if_stopped()

        start_time = time.time()
        self.state_manager.update_state("progress", "Раскладываем посты по категориям")
        filtered_posts = post_analyzer.posts_analyze(posts)
        logger.info(f"Time to process posts: {(time.time() - start_time)}")

        self.task_manager.raise_if_stopped()
        report_creator.generate_reports(filtered_posts)
