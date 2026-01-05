from collections import defaultdict

from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class PostCategorizer:
    """Категоризует посты по длине текста."""

    def __init__(self):
        """Создаёт набор категорий по диапазонам длины."""
        self.categories = {
            PostCategory(0, 400, 8, 10),
            PostCategory(400, 1200, 4, 6),
            PostCategory(1200, 2500, 2, 2),
            PostCategory(2500, float("inf"), 1, 1),
        }

    def categorize_post(self, text_length: int) -> PostCategory | None:
        """Определяет категорию поста по длине.

        Args:
            text_length (int): Длина текста поста.

        Returns:
            PostCategory | None: Найденная категория или None.

        """
        for category in self.categories:
            if category.max_length == float("inf"):
                if text_length >= category.min_length:
                    logger.debug("Category is defined")
                    return category
            elif category.min_length < text_length <= category.max_length:
                logger.debug("Category is defined")
                return category

        logger.error("Category is not defined")
        return None

    @staticmethod
    def categorize_posts(posts: list[Post]) -> dict[PostCategory, list[Post]]:
        """Группирует посты по категориям.

        Args:
            posts (list[Post]): Посты для группировки.

        Returns:
            dict[PostCategory, list[Post]]: Словарь категория → посты.

        """
        categorized_posts = defaultdict(list)

        for post in posts:
            categorized_posts[post.category].append(post)

        sorted_categorized_posts = dict(
            sorted(categorized_posts.items(), key=lambda item: item[0].min_length),
        )

        logger.info("Posts are divided into categories")
        return sorted_categorized_posts

    @staticmethod
    def calculate_points(category: PostCategory, post_count: int) -> int:
        """Вычисляет баллы за количество постов в категории.

        Args:
            category (PostCategory): Категория постов.
            post_count (int): Количество постов.

        Returns:
            int: Суммарные баллы.

        """
        first_part = post_count // category.max_value
        second_part = (post_count % category.max_value) // category.min_value
        result = first_part + second_part

        logger.debug(f'Points for "{category}" of posts are calculated {result}')

        return result
