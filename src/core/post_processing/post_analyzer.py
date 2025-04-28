from src.core.manager.state_manager import StateManager

from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.core.post_processing import PostCategorizer
from src.core.post_processing.author_validator import AuthorValidator
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.mapper.post_mapper import PostMapper

logger = setup_logger(__name__)


class PostAnalyzer:
    def __init__(self, state_manager: StateManager):
        # Validator for checking if the author of a post is valid
        self.state_manager = state_manager
        self.author_validator = AuthorValidator(self.state_manager.state.full_name)
        # Converts raw post data into Post model objects
        self.post_mapper = PostMapper()

    def posts_analyze(self, posts) -> dict[PostCategory, list[Post]]:
        # List to store valid mapped posts
        list_of_posts = []

        for post in posts:
            if self.author_validator.validate_author(
                post
            ):  # Check if the author is valid
                post_model = self.post_mapper.to_post_model(
                    post
                )  # Convert to Post model
                list_of_posts.append(post_model)

        self.state_manager.update_state("post_count", len(list_of_posts))
        logger.info("Posts are filtered and mapped to Post objects")

        # Sort posts by date in ascending order
        sorted_posts = sorted(list_of_posts, key=lambda post: post.date)
        logger.info("Posts are sorted")

        # Categorize posts into defined categories
        categorized_posts = PostCategorizer.categorize_posts(sorted_posts)

        return categorized_posts
