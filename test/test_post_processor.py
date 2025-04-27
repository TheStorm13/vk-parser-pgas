import re

import pytest


def create_pattern_v1(fio):
    surname, name, patronymic = fio.split()
    return re.compile(
        rf"Текст:\s*{surname}\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?|"
        rf"Текст:\s*{name[0]}(\.\s*{patronymic[0]}\.?|{name[1:]})?\s*{surname}",
        re.IGNORECASE
    )


def create_pattern_v2(fio):
    patronymic = None
    surname, name, patronymic = fio.split()

    prefix = r"(Автор|Текст)\s*:?\s*"

    # Инициалы, полное имя. Если отчество есть, оно опционально.
    name_variations = rf"({name[0]}\.?)|({name})"

    patronymic_variations = (
        rf"({patronymic[0]}\.?)|({patronymic})"
        if patronymic
        else ""
    )

    name_patronymic = rf"({name_variations}(\s*{patronymic_variations})?)"

    # Проверка фамилии + имя (и возможно отчество), игнорируя лишние пробелы
    name_and_surname = rf"({surname}\s+{name_patronymic})|({name_patronymic}\s+{surname})"

    pattern = rf"\b({prefix})({name_and_surname})\b"
    print(pattern)

    return re.compile(pattern, re.IGNORECASE)

def create_pattern_v3(fio):
    surname, name, patronymic = fio.split()

    prefix = r"(Автор|Текст)\s*:?\s*"

    # Handle full name and initial variations
    name_variations = rf"({name[0]}\.?\s*|{name}\s*)"
    patronymic_variations = rf"({patronymic[0]}\.?\s*|{patronymic}\s*)"

    # Pattern for both direct and reversed order
    direct_order = rf"{surname}\s+{name_variations}({patronymic_variations})?"
    reversed_order = rf"{name_variations}({patronymic_variations})?{surname}"

    # Combine patterns
    pattern = rf"^{prefix}({direct_order}|{reversed_order})\s*\.?\s*$"

    return re.compile(pattern, re.IGNORECASE)


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
    ("Текст: Иванов Иван", False),
    ("Текст: Гроза", False),
    ("Иванов Иван", False),
    ("Текст: Иван И", False),
    # === Успешные совпадения ===
    ("Текст: Гроза Илья Валерьевич", True),  # Полное совпадение с ФИО
    ("Текст: Гроза     Илья     Валерьевич", True),  # Лишние пробелы
    ("Автор: Гроза Илья", True),  # "Автор" вместо "Текст"
    ("Автор: Гроза И.", True),  # Сокращённое имя
    ("Текст: Гроза И.В.", True),  # Сокращённое имя и отчество
    ("Текст: Гроза И. В.", True),  # Сокращённое имя и отчество с пробелом
    ("Текст: Илья В. Гроза", True),  # Инвертированный порядок
    ("Текст: И. В. Гроза", True),  # Тоже инвертированный порядок
    ("Текст: Илья Гроза", True),  # Без отчества
    ("Текст: Гроза Илья Валерьевич.", True),  # Точка в конце
    ("Автор: Гроза ИльяВ.", True),  # Инициалы слитно с фамилией
    ("Автор:   Гроза   И. В.   ", True),  # Лишние пробелы везде
    ("Текст: Гроза И.Валерьевич", True),  # Стирается пробел между инициалами
    ("Текст: Гроза И.    В.", True),  # Лишние пробелы между инициалами
    ("Текст:  Гроза Илья Валерьевич  ", True),  # Лишние пробелы в начале и конце

    # === Несовпадения ===
    ("Текст: Иванов Иван", False),  # Другой автор
    ("Автор: Иванов", False),  # Нет имени и отчества
    ("Текст: Илья", False),  # Нет фамилии
    ("Текст: Гроза Иван Иванович", False),  # Нет имени "Илья"
    ("Текст: Гроз Илья Валерьевич", False),  # Ошибка в фамилии
    ("Автор: Гроза Иль", False),  # Неполное имя
    ("Текст: Гроза Ив. Валерьевич", False),  # Неправильные инициалы
    ("Текст: Гроза Иванович", False),  # Нет имени, только отчество
    ("Текст: И. Иванович", False),  # Только имя с инициалом
    ("Текст: Иванович Гроза", False),  # Отчество перед фамилией
    ("Текст: Гроза Илья Валерий", False),  # Ошибка в отчестве
    ("Something else entirely", False),  # Строка другого содержания
    ("Гроза Илья Валерьевич", False),  # Префикс "Текст" или "Автор" отсутствует
    ("Автор: Гроза + Илья", False),  # Неожиданный символ "+"
    ("", False),  # Пустая строка

    # === Граничные случаи ===
    ("Текст: Гроза-Илья Валерьевич", False),  # Слитное написание фамилии и имени с дефисом
    ("Текст: Гроза И-В.", False),  # Инициалы с дефисом
    ("Текст: Гроза, И. В.", False),  # Лишняя запятая
    ("Текст: Гроза Илья!", False),  # Восклицательный знак
    ("Текст: Гроза-Илья", False),  # Слитное имя и фамилия через дефис
    ("Автор: Гроза    И В ", True),  # Отдельные буквы имени и отчества с пробелами

])
def test_pattern_matching(text, expected):
    fio = "Гроза Илья Валерьевич"

    # pattern = create_pattern_v1(fio)
    # assert (pattern.search(text) is not None) == expected

    pattern = create_pattern_v3(fio)
    print(pattern)

    assert (pattern.search(text) is not None) == expected
