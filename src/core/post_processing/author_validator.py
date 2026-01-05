import re
from re import Match

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class AuthorValidator:
    """Проверяет упоминание автора в тексте и комментариях.

    Args:
        full_name (str): ФИО через пробел.

    """

    def __init__(self, full_name):
        """Создаёт валидатор и компилирует шаблоны.

        Args:
            full_name (str): ФИО через пробел.

        """
        self.full_name = full_name
        self.pattern_fio = self.create_pattern_fio(full_name)
        self.pattern_fi = self.create_pattern_fi(full_name)

    @staticmethod
    def create_pattern_fi(full_name: str) -> re.Pattern:
        """Строит шаблон для «Фамилия Имя/инициал».

        Args:
            full_name (str): ФИО через пробел.

        Returns:
            re.Pattern: Компилированный шаблон.

        Raises:
            ValueError: Некорректный формат ФИО.

        """
        try:
            surname, name, patronymic = full_name.split()
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            raise ValueError("Неправильно введено Фамилия имя!")

        prefix = r"((Автор|Текст)\s*:?\s*)"

        # Обрабатывает полное имя и инициалы
        name_variations = rf"(({name[0]}\.?)|({name}))\s*"

        # Поддерживает прямой и обратный порядок
        direct_order = rf"({surname}\s*{name_variations})"
        reversed_order = rf"({name_variations}{surname})"

        # Комбинирует подшаблоны
        pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*(\.|\s|$)\s*)"

        return re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def create_pattern_fio(full_name: str) -> re.Pattern:
        """Строит шаблон для «Фамилия Имя Отчество/инициалы».

        Args:
            full_name (str): ФИО через пробел.

        Returns:
            re.Pattern: Компилированный шаблон.

        Raises:
            ValueError: Некорректный формат ФИО.

        """
        try:
            surname, name, patronymic = full_name.split()
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            raise ValueError("Неправильно введено Фамилия имя!")

        prefix = r"((Автор|Текст)\s*:?\s*)"

        # Обрабатывает полное имя и инициалы
        name_variations = rf"(({name[0]}\.?)|({name}))\s*"
        patronymic_variations = rf"(({patronymic[0]}\.?)|({patronymic}))\s*"

        # Поддерживает прямой и обратный порядок
        direct_order = rf"({surname}\s*{name_variations}({patronymic_variations})?)"
        reversed_order = rf"({name_variations}({patronymic_variations})?{surname})"

        # Комбинирует подшаблоны
        pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*\.?\s*)"

        return re.compile(pattern, re.IGNORECASE)

    def check_author(self, text: str) -> Match[str] | None:
        """Ищет упоминание автора в тексте.

        Args:
            text (str): Исходный текст.

        Returns:
            Match | None: Совпадение или None.

        """
        result = self.pattern_fi.search(text) or self.pattern_fio.search(text)
        return result

    def validate_author(self, post) -> bool:
        """Проверяет упоминание автора в посте и комментариях.

        Args:
            post (dict): Объект поста VK.

        Returns:
            bool: True, если автор найден.

        """
        if self.check_author(post["text"]):
            logger.debug("The author is indicated in the text of the post")
            return True

        if post["comments"]["count"] > 0:
            comments = post["comments"]["items"]
            for comment in comments:
                if self.check_author(comment["text"]):
                    logger.debug("The author is indicated in the comments of the post")
                    return True

        logger.debug("The author is not discovered at the post")
        return False
