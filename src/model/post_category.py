class PostCategory:
    def __init__(self, min_length: int, max_length: int = None, min_value: int = None, max_value: int = None):
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"Пост (от {self.min_length} до {self.max_length} знаков)"
