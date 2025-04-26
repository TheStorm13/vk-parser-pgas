import time

from config_local import VK_TOKEN
from src.logger.logger import setup_logger
from src.logic.api_handlers.vk_api_handler import VKAPIHandler
from src.logic.post_processing.post_analyzer import PostAnalyzer
from src.report.report_creator import ReportCreator
from src.state.state_app import StateApp

logger = setup_logger(__name__)  # Initialize module-specific logger


class PostController:
    def __init__(self):
        pass

    def run(self, state: StateApp, update_progress=None):
        try:
            vk_handler = VKAPIHandler(state.vk_token)  # Handles interactions with VK API
            post_analyzer = PostAnalyzer(state.full_name)  # Analyzes posts specific to the given FIO
            report_creator = ReportCreator()  # Generates final reports from processed data

            # Fetch posts from VK
            start_time = time.time()
            posts = vk_handler.get_posts(
                state,
                update_progress)
            logger.info(f"Time to fetch posts: {(time.time() - start_time)}")

            # Analyze and filter posts
            start_time = time.time()
            filtered_posts = post_analyzer.posts_analyze(posts)
            logger.info(f"Time to process posts: {(time.time() - start_time)}")

            # Generate the report
            report_creator.generate_reports(filtered_posts, "result")

        except Exception as e:
            logger.error(e)
