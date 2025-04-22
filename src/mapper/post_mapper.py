from src.model.post import Post
from src.post_processing import PostCategorizer
from src.utils.data_utils import DataUtils
from src.utils.text_utils import TextUtils


class PostMapper:
    def __init__(self):
        self.post_categorize = PostCategorizer()

    def to_post_model(self, post) -> Post:
        title = TextUtils.extract_title(post['text'])
        post_text = post['text']
        len_text = TextUtils.count_chars_before_pattern(post_text)
        post_date = DataUtils.convert_date(post['date'])
        # todo: добавить рабочую ссылку
        url = TextUtils.get_post_link(post['from_id'], post['id'])
        category = self.post_categorize.categorize_post(len_text)

        post = Post(title, post_text, len_text, post_date, url, category)

        return post
