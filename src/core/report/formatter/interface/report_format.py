from abc import ABC, abstractmethod

from src.core.model.post import Post


class ReportFormat(ABC):
    """Определяет контракт форматирования отчёта."""

    @abstractmethod
    def format_header(self, count_posts: int) -> str:
        """Форматирует заголовок отчёта.

        Args:
            count_posts: Общее количество постов.

        Returns:
            Строку заголовка.

        """

    @abstractmethod
    def format_category_header(
            self, category_name: str, count_posts: int, category_point: int,
    ) -> str:
        """Форматирует заголовок категории.

        Args:
            category_name: Название категории.
            count_posts: Количество постов в категории.
            category_point: Порядковый номер категории.

        Returns:
            Строку заголовка категории.

        """

    @abstractmethod
    def format_post(self, post: Post) -> str:
        """Форматирует один пост.

        Args:
            post: Модель поста.

        Returns:
            Строку с постом.

        """

    @abstractmethod
    def format_category_posts(self, posts: list[Post]) -> str:
        """Форматирует список постов категории.

        Args:
            posts: Список моделей постов.

        Returns:
            Строку с постами категории.

        """
