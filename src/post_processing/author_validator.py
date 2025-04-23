import re


class AuthorValidator:
    def __init__(self, fio):
        # Разбиваем ФИО на части
        self.fio = fio

    @staticmethod
    def create_pattern(fio):
        # todo: добавить логирование и типизацию
        surname, name, _ = fio.split()

        # Префиксы: Автор или Текст, разделенные пробелами
        prefix = r"(Автор|Текст)\s*:?\s*"

        # Формат имени (инициалы или полное имя)
        name_variations = rf"{name[0]}\.?|{name}"

        # Фамилия или имя в различных вариантах
        name_and_surname = rf"({surname}\s*{name_variations}|{name_variations}\s*{surname})"

        # Финальное регулярное выражение
        return re.compile(
            rf"{prefix}{name_and_surname}",
            re.IGNORECASE
        )

    def check_author(self, text):
        # todo: добавить логирование и типизацию
        pattern = AuthorValidator.create_pattern(self.fio)
        return pattern.search(text)

    def validate_author(self, post):
        # todo: добавить логирование и типизацию

        # Проверяем текст поста
        if self.check_author(post['text']):
            return True

        # Получаем комментарии к посту
        if post['comments']['count'] > 0:
            comments = post['comments']['items']
            for comment in comments:
                # Проверяем текст комментария
                if self.check_author(comment['text']):
                    return True

        return False
