import re


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
        # todo: добавить логирование и типизацию
        """
        Формирует ссылку на пост.
        """
        return f"https://vk.com/wall{owner_id}_{post_id}"

    @staticmethod
    def remove_emoji(text: str, EMOJI_PATTERN=EMOJI_PATTERN):
        # todo: добавить логирование и типизацию
        """
        Удаляет emoji из текста.
        """
        return EMOJI_PATTERN.sub(r'', text)

    @staticmethod
    def extract_title(post_text: str):
        # todo: добавить логирование и типизацию
        """
        Извлекает название из шапки поста (первая строка текста) и удаляет emoji.
        """
        lines = post_text.split('\n')
        if lines:
            title = lines[0].strip()
            return TextUtils.remove_emoji(title)  # Удаляем emoji из названия
        return "Без названия"

    @staticmethod
    def count_chars_before_pattern(post_text: str):
        # todo: добавить логирование и типизацию
        """
        Считает количество символов до первого вхождения # или до конца текста, если # отсутствует.
        :param text: Текст поста.
        :return: Количество символов.
        """
        hash_index = post_text.find('#')  # Ищем индекс первого вхождения #
        if hash_index == -1:  # Если # не найден
            return len(post_text)  # Возвращаем длину всего текста
        return hash_index  # Возвращаем индекс первого #
