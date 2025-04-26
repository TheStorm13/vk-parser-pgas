from collections import defaultdict

from src.logger.logger import setup_logger
from src.model.post import Post
from src.model.post_category import PostCategory

logger = setup_logger(__name__)


class PostCategorizer:
    def __init__(self):
        # Define post categories with specific length ranges and values
        self.categories = {
            PostCategory(0, 400, 8, 10),
            PostCategory(400, 1200, 4, 6),
            PostCategory(1200, 2500, 2, 2),
            PostCategory(2500, float('inf'), 1, 1)

        }

    def categorize_post(self, text_length: int) -> PostCategory:
        # Determine the category for a post based on its length
        for category in self.categories:
            # Check if post belongs to an open-ended length category
            if category.max_length is float('inf'):
                if text_length >= category.min_length:
                    logger.debug("Category is defined")
                    return category

            # Check post length falls between specific min and max range
            elif category.min_length < text_length <= category.max_length:
                logger.debug("Category is defined")
                return category

        # If no category matches, log an error and return None
        logger.error("Category is not defined")
        return None

    @staticmethod
    def categorize_posts(posts: list[Post]) -> dict[PostCategory, list[Post]]:
        # Organize posts into categories
        categorized_posts = defaultdict(list)

        for post in posts:
            categorized_posts[post.category].append(post)

        # Sort categories by their minimum length for easier readability
        sorted_categorized_posts = dict(sorted(categorized_posts.items(), key=lambda item: item[0].min_length))

        logger.info("Posts are divided into categories")

        return sorted_categorized_posts

    @staticmethod
    def calculate_points(category: PostCategory, post_count: int) -> int:
        # Calculate points based on category values and post count
        first_part = (post_count // category.max_value)  # Full sets matching max value
        second_part = (post_count % category.max_value) // category.min_value  # Partial sets
        result = first_part + second_part

        logger.debug(f"Points for \"{category}\" of posts are calculated {result}")

        return result
