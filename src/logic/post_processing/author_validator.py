import re

from src.logger.logger import setup_logger

logger = setup_logger(__name__)


class AuthorValidator:
    def __init__(self, fio):
        self.fio = fio

    @staticmethod
    def create_pattern(fio: str) -> re.Pattern:
        # Create a regex pattern to match the author name in the text
        surname, name, _ = fio.split()

        prefix = r"(Автор|Текст)\s*:?\s*"  # Match "Author" or "Text" with optional colons/spaces

        name_variations = rf"{name[0]}\.?|{name}"  # Initial or full name of the author

        name_and_surname = rf"({surname}\s*{name_variations}|{name_variations}\s*{surname})"

        return re.compile(
            rf"{prefix}{name_and_surname}",
            re.IGNORECASE
        )

    def check_author(self, text: str):
        # Check if the author name appears in the provided text
        pattern = AuthorValidator.create_pattern(self.fio)
        result = pattern.search(text)

        return result

    def validate_author(self, post) -> bool:
        # Validate if the author is mentioned in the post or its comments
        if self.check_author(post['text']):
            logger.debug("The author is indicated in the text of the post")
            return True

        # Check each comment for the author name
        if post['comments']['count'] > 0:
            comments = post['comments']['items']
            for comment in comments:
                if self.check_author(comment['text']):
                    logger.debug("The author is indicated in the comments of the post")
                return True

        logger.debug("The author is not discovered at the post")
        return False
