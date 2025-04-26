from src.logger.logger import setup_logger
from src.logic.post_processing import PostCategorizer
from src.logic.post_processing.author_validator import AuthorValidator
from src.mapper.post_mapper import PostMapper
from src.model.post import Post
from src.model.post_category import PostCategory

logger = setup_logger(__name__)


class PostAnalyzer:
    def __init__(self, fio):
        # Validator for checking if the author of a post is valid
        self.author_validator = AuthorValidator(fio)
        # Converts raw post data into Post model objects
        self.post_mapper = PostMapper()

    def posts_analyze(self, posts) -> dict[PostCategory, list[Post]]:
        # List to store valid mapped posts
        list_of_posts = []

        for post in posts:
            if self.author_validator.validate_author(post):  # Check if the author is valid
                post_model = self.post_mapper.to_post_model(post)  # Convert to Post model
                list_of_posts.append(post_model)

        logger.info("Posts are filtered and mapped to Post objects")

        # Sort posts by date in ascending order
        sorted_posts = sorted(list_of_posts, key=lambda post: post.date)
        logger.info("Posts are sorted")

        # Categorize posts into defined categories
        categorized_posts = PostCategorizer.categorize_posts(sorted_posts)

        return categorized_posts
