from src.core.model.post import Post
from src.core.report.formatter.interface.report_format import ReportFormat
from src.infrastructure.utils.data_utils import DateUtils


class TextReportFormat(ReportFormat):
    """Форматирует отчеты в текстовом виде."""

    def format_header(self, count_posts: int) -> str:
        """Форматирует заголовок отчета.

        Args:
            count_posts: Количество постов (int).

        Returns:
            Готовый заголовок текста.

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
            f"{'-' * 40}\n"
        )

    def format_post(self, post: Post) -> str:
        """Форматирует блок данных поста.

        Args:
            post: Модель поста (Post).

        Returns:
            Текстовый блок поста.

        """
        post_date = DateUtils.datetime_to_string(post.date)

        return (
            f"Название: {post.title}\n"
            f"Дата: {post_date}\n"
            f"Количество символов: {post.len_text}\n"
            f"Ссылка на пост: {post.url}\n"
            f"{'-' * 40}\n"
        )

    def format_category_posts(self, posts: list[Post]) -> str:
        """Собирает блоки постов категории.

        Args:
            posts: Список постов (list[Post]).

        Returns:
            Конкатенированные блоки постов.

        """
        return "".join(self.format_post(post) for post in posts)
