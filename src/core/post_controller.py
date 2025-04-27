import time


from src.core.api_handlers.vk_api_handler import VKAPIHandler
from src.core.manager.state_manager import StateManager
from src.core.post_processing.post_analyzer import PostAnalyzer
from src.core.report.report_creator import ReportCreator
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)  # Initialize module-specific logger


class PostController:
    def __init__(self):
        pass

    def run(self, state_manager: StateManager):
        try:
            vk_handler = VKAPIHandler(state_manager)  # Handles interactions with VK API
            post_analyzer = PostAnalyzer(state_manager)  # Analyzes posts specific to the given FIO
            report_creator = ReportCreator()  # Generates final reports from processed data

            # Fetch posts from VK
            start_time = time.time()
            posts = vk_handler.get_posts()
            logger.info(f"Time to fetch posts: {(time.time() - start_time)}")

            # Analyze and filter posts
            start_time = time.time()
            filtered_posts = post_analyzer.posts_analyze(posts)
            logger.info(f"Time to process posts: {(time.time() - start_time)}")

            # Generate the report
            report_creator.generate_reports(filtered_posts, "result")

        except Exception as e:
            logger.error(e)
