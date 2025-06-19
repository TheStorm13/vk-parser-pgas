import re

from src.infrastructure.logger.logger import setup_logger

logger = setup_logger(__name__)


class AuthorValidator:
    def __init__(self, full_name):
        self.full_name = full_name
        self.pattern_fio = self.create_pattern_fio(full_name)
        self.pattern_fi = self.create_pattern_fi(full_name)

    @staticmethod
    def create_pattern_fi(full_name: str) -> re.Pattern:
        try:
            surname, name, patronymic = full_name.split()
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            raise ValueError("Неправильно введено Фамилия имя!")

        prefix = r"((Автор|Текст)\s*:?\s*)"

        # Handle full name and initial variations
        name_variations = rf"(({name[0]}\.?)|({name}))\s*"

        # Pattern for both direct and reversed order
        direct_order = rf"({surname}\s*{name_variations})"
        reversed_order = rf"({name_variations}{surname})"

        # Combine patterns
        pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*(\.|\s|$)\s*)"

        return re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def create_pattern_fio(full_name: str) -> re.Pattern:
        try:
            surname, name, patronymic = full_name.split()
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            raise ValueError("Неправильно введено Фамилия имя!")

        prefix = r"((Автор|Текст)\s*:?\s*)"

        # Handle full name and initial variations
        name_variations = rf"(({name[0]}\.?)|({name}))\s*"
        patronymic_variations = rf"(({patronymic[0]}\.?)|({patronymic}))\s*"

        # Pattern for both direct and reversed order
        direct_order = rf"({surname}\s*{name_variations}({patronymic_variations})?)"
        reversed_order = rf"({name_variations}({patronymic_variations})?{surname})"

        # Combine patterns
        pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*\.?\s*)"

        return re.compile(pattern, re.IGNORECASE)

    def check_author(self, text: str):
        # Check if the author name appears in the provided text
        result = self.pattern_fi.search(text) or self.pattern_fio.search(text)

        return result

    def validate_author(self, post) -> bool:
        # Validate if the author is mentioned in the post or its comments
        if self.check_author(post["text"]):
            logger.debug("The author is indicated in the text of the post")
            return True

        # Check each comment for the author name
        if post["comments"]["count"] > 0:
            comments = post["comments"]["items"]
            for comment in comments:
                if self.check_author(comment["text"]):
                    logger.debug("The author is indicated in the comments of the post")
                    return True

        logger.debug("The author is not discovered at the post")
        return False
