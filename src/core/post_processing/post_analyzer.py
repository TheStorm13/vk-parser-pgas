from src.core.manager.state_manager import StateManager
from src.core.model.post import Post
from src.core.model.post_category import PostCategory
from src.core.post_processing import PostCategorizer
from src.core.post_processing.author_validator import AuthorValidator
from src.infrastructure.logger.logger import setup_logger
from src.infrastructure.mapper.post_mapper import PostMapper

logger = setup_logger(__name__)


class PostAnalyzer:
    """Анализирует посты и распределяет их по категориям.

    Args:
        state_manager (StateManager): Менеджер состояния приложения.

    """

    def __init__(self, state_manager: StateManager):
        """Инициализирует зависимости анализатора.

        Args:
            state_manager (StateManager): Менеджер состояния.

        """
        self.state_manager = state_manager
        self.author_validator = AuthorValidator(self.state_manager.state.full_name)
        self.post_mapper = PostMapper()

    def posts_analyze(self, posts) -> dict[PostCategory, list[Post]]:
        """Фильтрует, преобразует и категоризует посты.

        Args:
            posts: Сырые посты VK.

        Returns:
            dict[PostCategory, list[Post]]: Категории и посты.

        """
        list_of_posts = []

        for post in posts:
            if self.author_validator.validate_author(post):
                post_model = self.post_mapper.to_post_model(post)
                list_of_posts.append(post_model)

        self.state_manager.update_state("post_count", len(list_of_posts))
        logger.info("Posts are filtered and mapped to Post objects")

        sorted_posts = sorted(list_of_posts, key=lambda post: post.date)
        logger.info("Posts are sorted")

        categorized_posts = PostCategorizer.categorize_posts(sorted_posts)

        return categorized_posts
