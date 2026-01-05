from src.core.model.post import Post
from src.core.post_processing import PostCategorizer
from src.infrastructure.utils.data_utils import DateUtils
from src.infrastructure.utils.text_utils import TextUtils


class PostMapper:
    """Преобразует данные постов в модель Post."""

    def __init__(self):
        self.post_categorizer = PostCategorizer()

    def to_post_model(self, post) -> Post:
        """Преобразует сырые данные поста в модель Post.

        Args:
            post (dict): Сырые данные поста.

        Returns:
            Post: Модель Post.

        """
        title = TextUtils.extract_title(post["text"])
        post_text = post["text"]
        len_text = TextUtils.count_chars_before_pattern(post_text)
        post_date = DateUtils.timestamp_to_datetime(post["date"])
        url = TextUtils.get_post_link(post["from_id"], post["id"])
        category = self.post_categorizer.categorize_post(len_text)
        post = Post(title, post_text, len_text, post_date, url, category)

        return post
