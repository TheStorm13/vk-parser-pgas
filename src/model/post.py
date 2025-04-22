from datetime import datetime

from src.model.post_category import PostCategory
from src.utils.data_utils import DataUtils


class Post:
    def __init__(
            self,
            title: str,
            post_text: str,
            len_text: int,
            date: datetime,
            url: str,
            category: PostCategory
    ):
        self.title = title
        self.post_text = post_text
        self.len_text = len_text
        self.date = date
        self.url = url
        self.category = category

    def __str__(self):
        # Возвращаем строковое представление поста, включающее его основные атрибуты
        return (f"Post(title='{self.title}', date={DataUtils.format_date(self.date)}"
                f"url='{self.url}', category='{self.category.__str__()}', text_length={self.len_text})")
