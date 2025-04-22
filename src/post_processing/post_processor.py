import re

from src.post_processing.text_utils import TextUtils


class PostProcessor:
    def __init__(self, fio):
        # Разбиваем ФИО на части
        surname, name, patronymic = fio.split()

        # Создаем регулярное выражение с учетом ФИО
        self.author_pattern = re.compile(
            rf"Текст:\s*{surname}\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?|"
            rf"Текст:\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?\s*{surname}",
            re.IGNORECASE
        )

    def filter_posts(self, posts):
        """
        Фильтрует посты, оставляя только те, где есть указанный текст в посте или комментариях.
        :param posts: Список постов.
        :return: Отфильтрованный список постов.
        """
        filtered_posts = []
        for post in posts:
            # Проверяем текст поста
            if self.author_pattern.search(post['text']):
                filtered_posts.append(post)
                continue  # Если паттерн найден в посте, пропускаем проверку комментариев

            # Получаем комментарии к посту
            if post['comments']['count'] > 0:
                comments = post['comments']['items']
                for comment in comments:
                    # Проверяем текст комментария
                    if self.author_pattern.search(comment['text']):
                        filtered_posts.append(post)
                        break  # Если паттерн найден в комментарии, добавляем пост и выходим из цикла

        return filtered_posts

    def extract_title(self, post_text):
        """
        Извлекает название из шапки поста (первая строка текста) и удаляет emoji.
        """
        lines = post_text.split('\n')
        if lines:
            title = lines[0].strip()
            return TextUtils.remove_emoji(title)  # Удаляем emoji из названия
        return "Без названия"

    def count_chars_before_pattern(self, post_text):
        """
        Считает количество символов до первого вхождения # или до конца текста, если # отсутствует.
        :param text: Текст поста.
        :return: Количество символов.
        """
        hash_index = post_text.find('#')  # Ищем индекс первого вхождения #
        if hash_index == -1:  # Если # не найден
            return len(post_text)  # Возвращаем длину всего текста
        return hash_index  # Возвращаем индекс первого #
