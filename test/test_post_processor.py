import re
import pytest

# Регулярное выражение на основе ФИО
def create_pattern_v1(fio):
    surname, name, patronymic = fio.split()
    return re.compile(
        rf"Текст:\s*{surname}\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?|"
        rf"Текст:\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?\s*{surname}",
        re.IGNORECASE
    )

def create_pattern_v2(fio):
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



# Тестовые данные
@pytest.mark.parametrize("text, expected", [
    ("Текст: Гроза И. В.", True),
    ("Текст: Гроза Илья", True),
    ("Текст: И. В. Гроза", True),
    ("Текст: Илья Гроза", True),
    ("Текст: Гроза И. Валерьевич", True),
    ("Текст: Гроза И В", True),
    ("Текст: Гроза И", True),
    ("Текст: И Гроза", True),
    ("Текст: Гроза И.В.", True),
    ("Текст: И.В. Гроза", True),
    ("Текст: Гроза И.    В.", True),
    ("Текст:Гроза  И. В.", True),
    ("Текст:   Гроза И    В.", True),
    ("Текст:  Илья  Гроза  ", True),
    ("Текст: И. В.   Гроза", True),
    ("Текст: Неправильный Текст", False),
])
def test_pattern_matching(text, expected):
    fio = "Гроза Илья Валерьевич"

    pattern = create_pattern_v1(fio)
    assert (pattern.search(text) is not None) == expected

    pattern = create_pattern_v2(fio)
    assert (pattern.search(text) is not None) == expected