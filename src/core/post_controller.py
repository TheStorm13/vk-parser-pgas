import time

from src.core.api_handlers.vk_api_handler import VKAPIHandler
from src.core.exception.task_interrupted_exception import TaskInterruptedException
from src.core.manager.state_manager import StateManager
from src.core.manager.task_manager import TaskManager
from src.core.post_processing.post_analyzer import PostAnalyzer
from src.core.report.report_creator import ReportCreator
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)  # Initialize module-specific logger


class PostController:
    def __init__(self,state_manager: StateManager, task_manager: TaskManager):
        self.state_manager=state_manager
        self.task_manager=task_manager

    def run(self):
        try:
            vk_handler = VKAPIHandler(self.state_manager,self.task_manager)  # Handles interactions with VK API
            post_analyzer = PostAnalyzer(self.state_manager)  # Analyzes posts specific to the given FIO
            report_creator = ReportCreator(self.state_manager)  # Generates final reports from processed data

            # Fetch posts from VK
            start_time = time.time()
            posts = vk_handler.get_posts()
            logger.info(f"Time to fetch posts: {(time.time() - start_time)}")

            # Analyze and filter posts
            self.task_manager.raise_if_stopped()


            start_time = time.time()
            filtered_posts = post_analyzer.posts_analyze(posts)
            logger.info(f"Time to process posts: {(time.time() - start_time)}")

            self.task_manager.raise_if_stopped()
            # Generate the report
            report_creator.generate_reports(filtered_posts)

        except TaskInterruptedException:
            raise TaskInterruptedException("Task was interrupted by the user.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

