from src.logger.logger import setup_logger
from src.logic.post_processing import PostCategorizer
from src.model.post import Post
from src.model.post_category import PostCategory
from src.report.formatter.interface.report_format import ReportFormat
from src.utils.data_utils import DataUtils

logger = setup_logger(__name__)


class ReportBuilder:
    def __init__(self, report_format: ReportFormat):
        self.report_format = report_format

    def build_report(self, result_posts: dict[PostCategory, list[Post]]) -> str:
        report = ""

        count_posts = sum(len(posts) for posts in result_posts.values())
        report += self.report_format.format_header(count_posts)

        for category, posts in result_posts.items():
            category_point = PostCategorizer.calculate_points(category, len(posts))
            report += self.report_format.format_category_header(category.__str__(), len(posts), category_point)

            report += self.report_format.format_category_posts(posts)

        return report

    @staticmethod
    def create_word_report(result_posts: dict[PostCategory, list[Post]]) -> str:
        """
        Создаёт таблицу из списка постов, используя знак новой строки для разделения строк.
        """
        output = f"Всего постов: {sum(len(posts) for posts in result_posts.values())}\n"

        for category, posts in result_posts.items():
            output += (f"\n\n\n{category}. Постов в категории: {len(posts)}\n")
            output += "Название\nДата\nСсылка\n"  # Используем табуляцию для разделения столбцов
            title_list = ""
            post_date_list = ""
            post_link_list = ""
            # Добавляем строки с данными
            for post in posts:
                title = post.title
                post_date = DataUtils.format_date(post.date)
                post_link = post.url

                title_list += f"\nПост «{title}»"
                post_date_list += f"\n{post_date}"
                post_link_list += f"\n{post_link}"

            # Форматируем строку
            output += title_list + post_date_list + post_link_list  # Добавляем новую строку

        return output
