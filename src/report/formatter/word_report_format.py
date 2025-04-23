from src.model.post import Post
from src.report.formatter.interface.report_format import ReportFormat
from src.utils.data_utils import DataUtils


class WordReportFormat(ReportFormat):
    def format_header(self, count_posts: int) -> str:
        return f"Всего постов: {count_posts}\n"

    def format_category_header(self, category_name: str, count_posts: int, category_point: int) -> str:
        return f"\n{category_name}\n" \
               f"Постов в категории: {count_posts}\n" \
               f"Количество баллов: {category_point}\n"

    def format_post(self, post: Post) -> dict:
        """
        Формирует словарь с названием, отформатированной датой и ссылкой поста.
        Они будут группироваться отдельно для каждой категории.
        """
        return {
            "title": f"Пост «{post.title}»",
            "date": DataUtils.format_date(post.date),
            "link": post.url
        }

    def format_category_posts(self, posts: list[Post]) -> str:
        """
        Формирует сначала список постов, затем список дат и другие данные.
        """
        # Сначала извлекаем отформатированные данные
        post_titles = [f"Пост «{post.title}»" for post in posts]
        post_dates = [f"{DataUtils.format_date(post.date)}" for post in posts]
        post_links = [f"{post.url}" for post in posts]

        # Формируем строки для вывода
        posts_section = "\nПосты:\n" + "\n".join(post_titles)
        dates_section = "Даты:\n" + "\n".join(post_dates)
        links_section = "Ссылки:\n" + "\n".join(post_links) + "\n"

        # Совмещаем все секции
        return f"{posts_section}\n\n{dates_section}\n\n{links_section}"
