from src.core.model.post import Post
from src.core.post_processing import PostCategorizer
from src.infrastructure.utils.data_utils import DateUtils
from src.infrastructure.utils.text_utils import TextUtils


class PostMapper:
    def __init__(self):
        self.post_categorizer = PostCategorizer()

    def to_post_model(self, post) -> Post:
        """
        Maps raw post data into a Post model.

        Args:
            post (dict): Dictionary containing raw post data.

        Returns:
            Post: Fully populated Post model object.
        """
        # Extract title from the post text
        title = TextUtils.extract_title(post['text'])

        # Fetch the raw post text
        post_text = post['text']

        # Calculate the length of the text before a specific pattern (e.g., a link)
        len_text = TextUtils.count_chars_before_pattern(post_text)

        # Convert date from the raw format into a standard date format
        post_date = DateUtils.timestamp_to_datetime(post['date'])

        # Generate a URL for the post using its ID and author ID
        url = TextUtils.get_post_link(post['from_id'], post['id'])

        # Categorize the post based on its text length
        category = self.post_categorizer.categorize_post(len_text)

        # Create a Post model using the transformed data
        post = Post(title, post_text, len_text, post_date, url, category)

        return post
