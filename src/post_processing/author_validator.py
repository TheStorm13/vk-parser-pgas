import re


class AuthorValidator:
    def __init__(self, fio):
        # Разбиваем ФИО на части
        surname, name, patronymic = fio.split()

        # Создаем регулярное выражение с учетом ФИО
        self.author_pattern = re.compile(
            rf"Текст:\s*{surname}\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?|"
            rf"Текст:\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?\s*{surname}",
            re.IGNORECASE
        )

    def check_author(self, text):
        return self.author_pattern.search(text['text'])

    def validate_author(self, post):
        # Проверяем текст поста
        if self.check_author(post):
            return True

        # Получаем комментарии к посту
        if post['comments']['count'] > 0:
            comments = post['comments']['items']
            for comment in comments:
                # Проверяем текст комментария
                if self.check_author(comment):
                    return True

        return False
