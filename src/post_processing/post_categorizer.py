from collections import defaultdict

from src.model.post import Post
from src.model.post_category import PostCategory


class PostCategorizer:
    def __init__(self):
        self.categories = {
            PostCategory(0, 400, 6, 8),
            PostCategory(400, 1200, 4, 6),
            PostCategory(1200, 2500, 2, 2),
            PostCategory(2500, None, 1, 1)

        }

    def categorize_post(self, len_text: int) -> PostCategory:
        """
        Классифицирует пост в категорию на основе его длины текста.
        :param post: Объект поста
        :return: Объект поста с обновленной категорией
        """
        for category in self.categories:
            if category.max_length is None:  # Для категории без верхнего предела длины
                if len_text >= category.min_length:
                    return category
            elif category.min_length < len_text <= category.max_length:
                return category
        return None

    @staticmethod
    def categorize_posts(posts: list[Post]):
        categorized_posts = defaultdict(list)
        for post in posts:
            categorized_posts[post.category].append(post)

        return categorized_posts

    @staticmethod
    def calculate_points(category: PostCategory, count_post: int) -> int:
        first_part = (count_post // category.max_value)
        second_part = (count_post % category.max_value) // category.min_value

        return first_part + second_part
