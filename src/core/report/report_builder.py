from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.core.post_processing import PostCategorizer
from src.core.report.formatter.interface.report_format import ReportFormat
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.utils.data_utils import DateUtils

logger = setup_logger(__name__)


class ReportBuilder:
    def __init__(self, report_format: ReportFormat):
        self.report_format = report_format

    def build_report(self, result_posts: dict[PostCategory, list[Post]]) -> str:
        """Builds a formatted report for given categorized posts."""
        report = ""

        # Calculate total posts and format the report header
        count_posts = sum(len(posts) for posts in result_posts.values())
        report += self.report_format.format_header(count_posts)

        # Process each category and add formatted category headers and posts
        for category, posts in result_posts.items():
            category_point = PostCategorizer.calculate_points(category, len(posts))
            report += self.report_format.format_category_header(category.__str__(), len(posts), category_point)

            report += self.report_format.format_category_posts(posts)

        return report

    @staticmethod
    def create_word_report(result_posts: dict[PostCategory, list[Post]]) -> str:
        """
        Creates a simple human-readable report in plain text.
        This report is not formatted with a specific ReportFormat instance.
        """
        output = f"Всего постов: {sum(len(posts) for posts in result_posts.values())}\n"

        for category, posts in result_posts.items():
            output += (f"\n\n\n{category}. Постов в категории: {len(posts)}\n")
            output += "Название\nДата\nСсылка\n"
            title_list = ""
            post_date_list = ""
            post_link_list = ""

            # Generate details for each post in the current category
            for post in posts:
                title = post.title
                post_date = DateUtils.datetime_to_string(post.date)
                post_link = post.url

                title_list += f"\nПост «{title}»"
                post_date_list += f"\n{post_date}"
                post_link_list += f"\n{post_link}"

            # Combine all lists into the output
            output += title_list + post_date_list + post_link_list

        return output
