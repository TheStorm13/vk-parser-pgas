from src.core.model.post import Post
from src.core.report.formatter.interface.report_format import ReportFormat
from src.infrastructure.utils.data_utils import DateUtils


class MarkdownReportFormat(ReportFormat):
    """Форматирует отчеты в Markdown."""

    def format_header(self, count_posts: int) -> str:
        """Форматирует заголовок отчета.

        Args:
            count_posts: Количество постов (int).

        Returns:
            Готовый заголовок Markdown.

        """
        return f"# Всего постов: {count_posts}\n"

    def format_category_header(
            self, category_name: str, count_posts: int, category_point: int,
    ) -> str:
        """Форматирует заголовок категории.

        Args:
            category_name: Имя категории (str).
            count_posts: Количество постов категории.
            category_point: Сумма баллов категории.

        Returns:
            Заголовок категории в Markdown.

        """
        return (
            f"## {category_name}\n"
            f"### Постов в категории: {count_posts}\n"
            f"### Количество баллов: {category_point}\n"
            "\n| Название | Длина | Дата | Ссылка |\n|------|------|------|------|\n"
        )

    def format_post(self, post: Post) -> str:
        """Форматирует строку таблицы поста.

        Args:
            post: Модель поста (Post).

        Returns:
            Строка таблицы Markdown.

        """
        title = post.title.replace("|", r"\|")
        post_date = DateUtils.datetime_to_string(post.date)
        return (
            f"| {title} | {post.len_text} | {post_date} | [{post.url}]({post.url}) |\n"
        )

    def format_category_posts(self, posts: list[Post]) -> str:
        """Собирает строки постов категории.

        Args:
            posts: Список постов (list[Post]).

        Returns:
            Конкатенированные строки таблицы.

        """
        return "".join(self.format_post(post) for post in posts)
