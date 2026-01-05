import re


class TextUtils:
    """Утилиты для обработки текста."""

    EMOJI_PATTERN = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # Эмодзи со смайлами
        "\U0001f300-\U0001f5ff"  # Символы и пиктограммы
        "\U0001f680-\U0001f6ff"  # Транспорт и карты
        "\U0001f700-\U0001f77f"  # Алхимические символы
        "\U0001f780-\U0001f7ff"  # Геометрические фигуры
        "\U0001f800-\U0001f8ff"  # Дополнительные символы
        "\U0001f900-\U0001f9ff"  # Дополнительные символы 2
        "\U0001fa00-\U0001fa6f"  # Шахматные символы
        "\U0001fa70-\U0001faff"  # Символы и пиктограммы 2
        "\U00002702-\U000027b0"  # Дингбаты
        "\U000024c2-\U0001f251"  # Заключённые в рамку
        "]+",
        flags=re.UNICODE,
    )

    @staticmethod
    def get_post_link(owner_id, post_id):
        """Формирует ссылку на пост VK.

        Args:
            owner_id (int | str): Идентификатор автора.
            post_id (int | str): Идентификатор поста.

        Returns:
            str: URL поста.

        """
        return f"https://vk.com/wall{owner_id}_{post_id}"

    @staticmethod
    def remove_emoji(text: str, EMOJI_PATTERN=EMOJI_PATTERN):
        """Удаляет эмодзи из текста.

        Args:
            text (str): Исходный текст.

        Returns:
            str: Текст без эмодзи.

        """
        return EMOJI_PATTERN.sub(r"", text)

    @staticmethod
    def extract_title(post_text: str):
        """Извлекает первую строку без эмодзи.

        Args:
            post_text (str): Полный текст поста.

        Returns:
            str: Заголовок без эмодзи.

        """
        lines = post_text.split("\n")

        if lines:
            title = lines[0].strip()
            return TextUtils.remove_emoji(title)

        return "Без названия"

    @staticmethod
    def count_chars_before_pattern(post_text: str):
        """Вычисляет длину до первого символа '#'.

        Args:
            post_text (str): Текст поста.

        Returns:
            int: Количество символов.

        """
        hash_index = post_text.find("#")

        if hash_index == -1:
            return len(post_text)

        return hash_index
