import re
from pickle import FALSE

import pytest


def create_pattern_v1(full_name):
    surname, name, patronymic = full_name.split()
    return re.compile(
        rf"Текст:\s*{surname}\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?|"
        rf"Текст:\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?\s*{surname}",
        re.IGNORECASE
    )


def create_pattern_v2(full_name):
    patronymic = None
    surname, name, patronymic = full_name.split()

    prefix = r"(Автор|Текст)\s*:?\s*"

    name_variations = rf"({name[0]}\.?)|({name})"

    patronymic_variations = (
        rf"({patronymic[0]}\.?)|({patronymic})"
        if patronymic
        else ""
    )

    name_patronymic = rf"({name_variations}(\s*{patronymic_variations})?)"

    name_and_surname = rf"({surname}\s+{name_patronymic})|({name_patronymic}\s+{surname})"

    pattern = rf"\b({prefix})({name_and_surname})\b"
    print(pattern)

    return re.compile(pattern, re.IGNORECASE)


def create_pattern_v3(full_name):
    surname, name, patronymic = full_name.split()

    prefix = r"((Автор|Текст)\s*:?\s*)"

    # Handle full name and initial variations
    name_variations = rf"(({name[0]}\.?)|({name}))\s*"
    patronymic_variations = rf"(({patronymic[0]}\.?)|({patronymic}))\s*"

    # Pattern for both direct and reversed order
    direct_order = rf"({surname}\s*{name_variations}({patronymic_variations})?)"
    reversed_order = rf"({name_variations}({patronymic_variations})?{surname})"

    # Combine patterns
    pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*\.?\s*)"
    print(pattern)

    return re.compile(pattern, re.IGNORECASE)

def create_pattern_v4(full_name):
    surname, name = full_name.split()

    prefix = r"((Автор|Текст)\s*:?\s*)"

    # Handle full name and initial variations
    name_variations = rf"(({name[0]}\.?)|({name}))\s*"

    # Pattern for both direct and reversed order
    direct_order = rf"({surname}\s*{name_variations})"
    reversed_order = rf"({name_variations}{surname})"

    # Combine patterns
    pattern = rf"(\s*{prefix}({direct_order}|{reversed_order})\s*\.?\s*(\s|$))"
    print(pattern)

    return re.compile(pattern, re.IGNORECASE)



# Test cases for verifying correctness of regex patterns
@pytest.mark.parametrize("text, expected", [
    # Test cases for positive matches
    ("Текст: Гроза И. ", True),  # Initial and surname
    ("Текст: Гроза Илья", True),  # Full name
    ("Текст: И.  Гроза", True),  # Reversed order with initial
    ("Текст: Илья Гроза", True),  # Reversed order
    ("Текст: Гроза И.", True),  # Shortened name
    ("Текст: И.Гроза", True),  # Without space
    ("Текст: Гроза     Илья     ", True),  # Extra spaces
    ("Автор: Гроза И.", True),  # Prefix "Author" instead of "Text"
    ("Автор:   Гроза   И.    ", True),  # Extra spaces everywhere

    # Test cases for negative matches
    ("Текст: Иванов Иван", False),  # Different author
    ("Автор: Иванов", False),  # Missing name and patronymic
    ("Текст: Гроза, И. В.", False),  # Extra comma
    ("Something else entirely", False),  # Unrelated text
    ("Текст: Гроза-Илья", False),  # Hyphenated name
    ("Текст: Гроза И-В.", False),  # Hyphenated initials
    ("", False)  # Empty string
])
def test_pattern_matching(text, expected):
    full_name = "Гроза Илья"  # Define full name for testing
    # Use the latest pattern version for testing
    pattern = create_pattern_v4(full_name)
    # Assert matching result matches the expected value
    assert (pattern.search(text) is not None) == expected
