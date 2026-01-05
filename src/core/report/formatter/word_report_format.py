from src.core.model.post import Post
from src.core.report.formatter.interface.report_format import ReportFormat
from src.infrastructure.utils.data_utils import DateUtils


class WordReportFormat(ReportFormat):
    """Форматирует данные отчета для Word."""

    def format_header(self, count_posts: int) -> str:
        """Форматирует заголовок отчета.

        Args:
            count_posts: Количество постов (int).

        Returns:
            Заголовок в текстовом виде.

        """
        return f"Всего постов: {count_posts}\n"

    def format_category_header(
            self, category_name: str, count_posts: int, category_point: int,
    ) -> str:
        """Форматирует заголовок категории.

        Args:
            category_name: Имя категории (str).
            count_posts: Количество постов категории.
            category_point: Сумма баллов категории.

        Returns:
            Заголовок категории в тексте.

        """
        return (
            f"\n{category_name}\n"
            f"Постов в категории: {count_posts}\n"
            f"Количество баллов: {category_point}\n"
        )

    def format_post(self, post: Post) -> dict:
        """Форматирует данные поста в словарь.

        Args:
            post: Модель поста (Post).

        Returns:
            Словарь полей поста.

        """
        return {
            "title": f"Пост «{post.title}»",
            "date": DateUtils.datetime_to_string(post.date),
            "link": post.url,
        }

    def format_category_posts(self, posts: list[Post]) -> str:
        """Собирает секции постов, дат и ссылок.

        Args:
            posts: Список постов (list[Post]).

        Returns:
            Текст категории с секциями.

        """
        post_titles = [
            # Нормализует пробелы и дубли в кавычках «»
            f"Пост «{post.title}»".replace("« ", "«").replace("»»", "»")
            for post in posts
        ]
        post_dates = [f"{DateUtils.datetime_to_string(post.date)}" for post in posts]
        post_links = [f"{post.url}" for post in posts]

        posts_section = "\nПосты:\n" + "\n".join(post_titles)
        dates_section = "Даты:\n" + "\n".join(post_dates)
        links_section = "Ссылки:\n" + "\n".join(post_links) + "\n"

        return f"{posts_section}\n\n{dates_section}\n\n{links_section}"
