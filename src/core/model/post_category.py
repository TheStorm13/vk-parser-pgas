class PostCategory:
    """Описывает категорию постов по длине и весам."""

    def __init__(
            self,
            min_length: int,
            max_length: int = float("inf"),
            min_value: int = None,
            max_value: int = None,
    ):
        """Создаёт категорию длины текста.

        Args:
            min_length (int): Минимальная длина.
            max_length (int | float): Максимальная длина.
            min_value (int | None): Минимальный вес.
            max_value (int | None): Максимальный вес.

        """
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        """Возвращает краткое текстовое представление."""
        return f"Пост (от {self.min_length} до {self.max_length} знаков)"
