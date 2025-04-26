import time

from config import VK_TOKEN, VK_GROUP
from src.logger.logger import setup_logger
from src.logic.api_handlers.vk_api_handler import VKAPIHandler
from src.logic.post_processing.post_analyzer import PostAnalyzer
from src.report.report_creator import ReportCreator

logger = setup_logger(__name__)  # Initialize module-specific logger


class PostController:
    def __init__(self):
        pass

    def run(self, fio, start_date, end_date, update_progress=None, group_name=VK_GROUP):
        """
        Main method to fetch, process, and generate a report on posts from VK.

        Args:
            fio: User information or identifier used by PostAnalyzer.
            start_date: Start date for fetching VK posts.
            end_date: End date for fetching VK posts.
            update_progress: Optional callback to update progress status.
            group_name: VK group from which posts are fetched. Defaults to VK_GROUP from config.
        """
        try:
            vk_handler = VKAPIHandler(VK_TOKEN)  # Handles interactions with VK API
            post_analyzer = PostAnalyzer(fio)  # Analyzes posts specific to the given FIO
            report_creator = ReportCreator()  # Generates final reports from processed data

            # Fetch posts from VK
            start_time = time.time()
            posts = vk_handler.get_posts(group_name, start_date, end_date, update_progress)
            logger.info(f"Time to fetch posts: {(time.time() - start_time)}")

            # Analyze and filter posts
            start_time = time.time()
            filtered_posts = post_analyzer.posts_analyze(posts)
            logger.info(f"Time to process posts: {(time.time() - start_time)}")

            # Generate the report
            report_creator.generate_reports(filtered_posts, "result")

        except Exception as e:
            logger.error(e)
