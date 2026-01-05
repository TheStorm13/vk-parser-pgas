from datetime import datetime

from src.core.model.post_category import PostCategory
from src.infrastructure.utils.data_utils import DateUtils


class Post:
    """Инкапсулирует данные поста.

    Attributes:
        title: Заголовок поста.
        post_text: Текст поста.
        len_text: Длина текста.
        date: Дата публикации.
        url: Ссылка на пост.
        category: Категория поста.

    """

    def __init__(
            self,
            title: str,
            post_text: str,
            len_text: int,
            date: datetime,
            url: str,
            category: PostCategory,
    ):
        """Создает экземпляр поста.

        Args:
            title: Заголовок поста.
            post_text: Текст поста.
            len_text: Длина текста.
            date: Дата публикации.
            url: Ссылка на пост.
            category: Категория поста.

        """
        self.title = title
        self.post_text = post_text
        self.len_text = len_text
        self.date = date
        self.url = url
        self.category = category

    def __str__(self):
        """Возвращает строковое представление.

        Returns:
            str: Форматированная строка.

        """
        return (
            f"Post(title='{self.title}', date={DateUtils.datetime_to_string(self.date)}, "
            f"url='{self.url}', category='{self.category.__str__()}', text_length={self.len_text})"
        )
