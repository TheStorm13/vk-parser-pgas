import re
from datetime import datetime


class TextUtils:
    EMOJI_PATTERN = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # эмодзи смайлов
        u"\U0001F300-\U0001F5FF"  # символы и пиктограммы
        u"\U0001F680-\U0001F6FF"  # транспорт и карты
        u"\U0001F700-\U0001F77F"  # алхимические символы
        u"\U0001F780-\U0001F7FF"  # геометрические фигуры
        u"\U0001F800-\U0001F8FF"  # дополнительные символы
        u"\U0001F900-\U0001F9FF"  # дополнительные символы
        u"\U0001FA00-\U0001FA6F"  # шахматы
        u"\U0001FA70-\U0001FAFF"  # символы и пиктограммы
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)

    @staticmethod
    def get_post_link(owner_id, post_id):
        """
        Формирует ссылку на пост.
        """
        return f"https://vk.com/wall{owner_id}_{post_id}"

    @staticmethod
    def format_date(timestamp):
        """
        Форматирует дату в формате DD.MM.YYYY.
        """
        return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y')

    @staticmethod
    def remove_emoji(text, EMOJI_PATTERN=EMOJI_PATTERN):
        """
        Удаляет emoji из текста.
        """
        return EMOJI_PATTERN.sub(r'', text)
